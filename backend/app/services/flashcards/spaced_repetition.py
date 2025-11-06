"""
Spaced Repetition Algorithms
Implements SM-2 and other algorithms for optimal review scheduling.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class SpacedRepetitionAlgorithm(ABC):
    """
    Abstract base class for spaced repetition algorithms.
    """

    @abstractmethod
    def calculate_next_review(
        self,
        state: Dict[str, Any],
        correct: bool
    ) -> Dict[str, Any]:
        """
        Calculate the next review schedule based on performance.

        Args:
            state: Current SR state (easiness_factor, interval_days, repetition_number)
            correct: Whether the answer was correct

        Returns:
            Updated state with new schedule
        """
        pass


class SM2Algorithm(SpacedRepetitionAlgorithm):
    """
    SuperMemo 2 (SM-2) Algorithm.

    The classic spaced repetition algorithm that adjusts intervals
    based on the quality of recall.
    """

    def calculate_next_review(
        self,
        state: Dict[str, Any],
        correct: bool
    ) -> Dict[str, Any]:
        """
        Calculate next review using SM-2 algorithm.

        Args:
            state: Current state with easiness_factor, interval_days, repetition_number
            correct: Whether the answer was correct

        Returns:
            Updated state with new interval and easiness factor
        """
        easiness_factor = state.get("easiness_factor", 2.5)
        interval_days = state.get("interval_days", 1)
        repetition_number = state.get("repetition_number", 0)

        # Quality of recall: 5 for perfect, 3 for correct with difficulty, 0 for incorrect
        quality = 4 if correct else 2

        # Update easiness factor
        new_ef = easiness_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_ef = max(1.3, new_ef)  # Minimum EF is 1.3

        # Calculate new interval
        if not correct:
            # Reset if incorrect
            new_interval = 1
            new_repetition = 0
        else:
            new_repetition = repetition_number + 1

            if new_repetition == 1:
                new_interval = 1
            elif new_repetition == 2:
                new_interval = 6
            else:
                new_interval = round(interval_days * new_ef)

        return {
            "easiness_factor": round(new_ef, 2),
            "interval_days": new_interval,
            "repetition_number": new_repetition
        }


class AnkiAlgorithm(SpacedRepetitionAlgorithm):
    """
    Anki-style algorithm with graduating intervals.

    Simplified version of Anki's scheduling algorithm.
    """

    def __init__(
        self,
        learning_steps: list[int] = [1, 10],  # minutes
        graduating_interval: int = 1,  # days
        easy_interval: int = 4,  # days
        starting_ease: float = 2.5,
        easy_bonus: float = 1.3,
        interval_modifier: float = 1.0
    ):
        """
        Initialize Anki algorithm parameters.

        Args:
            learning_steps: Steps in minutes for learning phase
            graduating_interval: Interval after graduating from learning
            easy_interval: Interval when marked as easy
            starting_ease: Initial ease factor
            easy_bonus: Multiplier for easy responses
            interval_modifier: Global interval modifier
        """
        self.learning_steps = learning_steps
        self.graduating_interval = graduating_interval
        self.easy_interval = easy_interval
        self.starting_ease = starting_ease
        self.easy_bonus = easy_bonus
        self.interval_modifier = interval_modifier

    def calculate_next_review(
        self,
        state: Dict[str, Any],
        correct: bool
    ) -> Dict[str, Any]:
        """
        Calculate next review using Anki algorithm.

        Args:
            state: Current state
            correct: Whether the answer was correct

        Returns:
            Updated state
        """
        easiness_factor = state.get("easiness_factor", self.starting_ease)
        interval_days = state.get("interval_days", 0)
        repetition_number = state.get("repetition_number", 0)

        if not correct:
            # Lapsed - reset to learning
            return {
                "easiness_factor": max(1.3, easiness_factor - 0.2),
                "interval_days": 1,
                "repetition_number": 0
            }

        # Correct answer
        if repetition_number == 0:
            # First correct answer - graduate
            new_interval = self.graduating_interval
        else:
            # Calculate interval based on ease factor
            new_interval = max(1, round(interval_days * easiness_factor * self.interval_modifier))

        return {
            "easiness_factor": min(2.5, easiness_factor + 0.15),
            "interval_days": new_interval,
            "repetition_number": repetition_number + 1
        }
