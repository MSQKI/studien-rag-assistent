"""
Flashcard Manager
SQLite-based flashcard management with spaced repetition.
"""

import sqlite3
import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from pathlib import Path

from loguru import logger

from app.config import get_settings
from app.services.flashcards.spaced_repetition import SpacedRepetitionAlgorithm, SM2Algorithm


class FlashcardManager:
    """
    Manages flashcards with SQLite database.
    """

    def __init__(self, db_path: Optional[Path] = None):
        """
        Initialize flashcard manager.

        Args:
            db_path: Optional path to SQLite database
        """
        settings = get_settings()
        self.db_path = db_path or settings.flashcards_db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.sr_algorithm: SpacedRepetitionAlgorithm = SM2Algorithm()
        self._init_database()
        logger.info(f"Initialized flashcard manager with database: {self.db_path}")

    def _init_database(self) -> None:
        """
        Initialize database schema.
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Flashcards table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS flashcards (
                id TEXT PRIMARY KEY,
                subject TEXT NOT NULL,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                difficulty INTEGER DEFAULT 1,
                tags TEXT,
                document_id TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_reviewed TIMESTAMP,
                next_review TIMESTAMP,
                correct_count INTEGER DEFAULT 0,
                incorrect_count INTEGER DEFAULT 0,
                easiness_factor REAL DEFAULT 2.5,
                interval_days INTEGER DEFAULT 1,
                repetition_number INTEGER DEFAULT 0
            )
        """)

        # Review history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS review_history (
                id TEXT PRIMARY KEY,
                flashcard_id TEXT NOT NULL,
                reviewed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                correct BOOLEAN NOT NULL,
                time_spent_seconds INTEGER,
                FOREIGN KEY (flashcard_id) REFERENCES flashcards (id) ON DELETE CASCADE
            )
        """)

        # Create indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_flashcards_subject ON flashcards(subject)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_flashcards_next_review ON flashcards(next_review)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_review_history_flashcard ON review_history(flashcard_id)
        """)

        conn.commit()
        conn.close()

    def _get_connection(self) -> sqlite3.Connection:
        """
        Get database connection.

        Returns:
            SQLite connection
        """
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def create_flashcard(
        self,
        subject: str,
        question: str,
        answer: str,
        difficulty: int = 1,
        tags: Optional[List[str]] = None,
        document_id: Optional[str] = None
    ) -> str:
        """
        Create a new flashcard.

        Args:
            subject: Subject category
            question: Question text
            answer: Answer text
            difficulty: Initial difficulty (1-5)
            tags: Optional list of tags
            document_id: Optional source document ID

        Returns:
            Flashcard ID
        """
        flashcard_id = str(uuid.uuid4())
        tags_str = ",".join(tags) if tags else ""

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO flashcards
            (id, subject, question, answer, difficulty, tags, document_id, next_review)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            flashcard_id,
            subject,
            question,
            answer,
            difficulty,
            tags_str,
            document_id,
            datetime.utcnow().isoformat()
        ))

        conn.commit()
        conn.close()

        logger.info(f"Created flashcard: {flashcard_id}")
        return flashcard_id

    def get_flashcard(self, flashcard_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a flashcard by ID.

        Args:
            flashcard_id: Flashcard ID

        Returns:
            Flashcard data or None
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM flashcards WHERE id = ?", (flashcard_id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return self._row_to_dict(row)
        return None

    def list_flashcards(
        self,
        subject: Optional[str] = None,
        tag: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List flashcards with optional filters.

        Args:
            subject: Optional subject filter
            tag: Optional tag filter
            limit: Maximum number of results
            offset: Number of results to skip

        Returns:
            List of flashcards
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM flashcards WHERE 1=1"
        params = []

        if subject:
            query += " AND subject = ?"
            params.append(subject)

        if tag:
            query += " AND tags LIKE ?"
            params.append(f"%{tag}%")

        query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
        params.extend([limit, offset])

        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        return [self._row_to_dict(row) for row in rows]

    def get_next_due_flashcard(
        self,
        subject: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get the next flashcard due for review.

        Args:
            subject: Optional subject filter

        Returns:
            Next flashcard or None
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        now = datetime.utcnow().isoformat()
        query = """
            SELECT * FROM flashcards
            WHERE (next_review IS NULL OR next_review <= ?)
        """
        params = [now]

        if subject:
            query += " AND subject = ?"
            params.append(subject)

        query += """
            ORDER BY
                CASE WHEN next_review IS NULL THEN 0 ELSE 1 END,
                next_review ASC,
                (1.0 / (correct_count + 1)) * difficulty DESC
            LIMIT 1
        """

        cursor.execute(query, params)
        row = cursor.fetchone()
        conn.close()

        if row:
            return self._row_to_dict(row)
        return None

    def record_answer(
        self,
        flashcard_id: str,
        correct: bool,
        time_spent_seconds: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Record an answer and update spaced repetition schedule.

        Args:
            flashcard_id: Flashcard ID
            correct: Whether the answer was correct
            time_spent_seconds: Optional time spent

        Returns:
            Updated flashcard data
        """
        flashcard = self.get_flashcard(flashcard_id)
        if not flashcard:
            raise ValueError(f"Flashcard not found: {flashcard_id}")

        # Update SR algorithm state
        sr_state = {
            "easiness_factor": flashcard["easiness_factor"],
            "interval_days": flashcard["interval_days"],
            "repetition_number": flashcard["repetition_number"]
        }

        new_state = self.sr_algorithm.calculate_next_review(sr_state, correct)

        # Calculate next review date
        next_review = datetime.utcnow() + timedelta(days=new_state["interval_days"])

        # Update flashcard
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE flashcards
            SET
                last_reviewed = ?,
                next_review = ?,
                correct_count = correct_count + ?,
                incorrect_count = incorrect_count + ?,
                easiness_factor = ?,
                interval_days = ?,
                repetition_number = ?,
                difficulty = CASE
                    WHEN ? THEN MAX(1, difficulty - 1)
                    ELSE MIN(5, difficulty + 1)
                END
            WHERE id = ?
        """, (
            datetime.utcnow().isoformat(),
            next_review.isoformat(),
            1 if correct else 0,
            0 if correct else 1,
            new_state["easiness_factor"],
            new_state["interval_days"],
            new_state["repetition_number"],
            correct,
            flashcard_id
        ))

        # Record in history
        review_id = str(uuid.uuid4())
        cursor.execute("""
            INSERT INTO review_history
            (id, flashcard_id, reviewed_at, correct, time_spent_seconds)
            VALUES (?, ?, ?, ?, ?)
        """, (
            review_id,
            flashcard_id,
            datetime.utcnow().isoformat(),
            correct,
            time_spent_seconds
        ))

        conn.commit()
        conn.close()

        logger.info(f"Recorded answer for flashcard {flashcard_id}: correct={correct}")
        return self.get_flashcard(flashcard_id)

    def update_flashcard(
        self,
        flashcard_id: str,
        question: Optional[str] = None,
        answer: Optional[str] = None,
        difficulty: Optional[int] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Update a flashcard.

        Args:
            flashcard_id: Flashcard ID
            question: Optional new question
            answer: Optional new answer
            difficulty: Optional new difficulty
            tags: Optional new tags

        Returns:
            Updated flashcard
        """
        flashcard = self.get_flashcard(flashcard_id)
        if not flashcard:
            raise ValueError(f"Flashcard not found: {flashcard_id}")

        conn = self._get_connection()
        cursor = conn.cursor()

        updates = []
        params = []

        if question is not None:
            updates.append("question = ?")
            params.append(question)

        if answer is not None:
            updates.append("answer = ?")
            params.append(answer)

        if difficulty is not None:
            updates.append("difficulty = ?")
            params.append(difficulty)

        if tags is not None:
            updates.append("tags = ?")
            params.append(",".join(tags))

        if updates:
            query = f"UPDATE flashcards SET {', '.join(updates)} WHERE id = ?"
            params.append(flashcard_id)
            cursor.execute(query, params)
            conn.commit()

        conn.close()
        return self.get_flashcard(flashcard_id)

    def delete_flashcard(self, flashcard_id: str) -> None:
        """
        Delete a flashcard.

        Args:
            flashcard_id: Flashcard ID
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM flashcards WHERE id = ?", (flashcard_id,))
        conn.commit()
        conn.close()

        logger.info(f"Deleted flashcard: {flashcard_id}")

    def get_stats(self) -> Dict[str, Any]:
        """
        Get flashcard statistics.

        Returns:
            Statistics dictionary
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        # Total flashcards
        cursor.execute("SELECT COUNT(*) as total FROM flashcards")
        total = cursor.fetchone()["total"]

        # Due today
        now = datetime.utcnow().isoformat()
        cursor.execute(
            "SELECT COUNT(*) as due FROM flashcards WHERE next_review <= ?",
            (now,)
        )
        due_today = cursor.fetchone()["due"]

        # Accuracy
        cursor.execute("""
            SELECT
                SUM(correct_count) as correct,
                SUM(incorrect_count) as incorrect
            FROM flashcards
        """)
        row = cursor.fetchone()
        correct = row["correct"] or 0
        incorrect = row["incorrect"] or 0
        total_reviews = correct + incorrect
        accuracy = (correct / total_reviews * 100) if total_reviews > 0 else 0.0

        # Study streak (days with at least one review)
        cursor.execute("""
            SELECT COUNT(DISTINCT DATE(reviewed_at)) as streak
            FROM review_history
            WHERE reviewed_at >= DATE('now', '-30 days')
        """)
        study_streak = cursor.fetchone()["streak"]

        conn.close()

        return {
            "total_flashcards": total,
            "due_today": due_today,
            "accuracy": round(accuracy, 1),
            "study_streak_days": study_streak,
            "total_reviews": total_reviews
        }

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        """
        Convert database row to dictionary.

        Args:
            row: SQLite row

        Returns:
            Dictionary representation
        """
        data = dict(row)

        # Parse tags
        if data.get("tags"):
            data["tags"] = data["tags"].split(",")
        else:
            data["tags"] = []

        return data


# Global flashcard manager instance
_flashcard_manager: Optional[FlashcardManager] = None


def get_flashcard_manager() -> FlashcardManager:
    """
    Get the global flashcard manager instance.

    Returns:
        FlashcardManager instance
    """
    global _flashcard_manager
    if _flashcard_manager is None:
        _flashcard_manager = FlashcardManager()
    return _flashcard_manager
