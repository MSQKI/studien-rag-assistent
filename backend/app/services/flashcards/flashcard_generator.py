"""
Flashcard Generator
Automatically generates flashcards from documents using LLM.
"""

from typing import List, Dict, Any
import json

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from loguru import logger

from app.config import get_settings
from app.services.flashcards.flashcard_manager import FlashcardManager, get_flashcard_manager


class FlashcardGenerator:
    """
    Generates flashcards from document content using LLM.
    """

    def __init__(self):
        """Initialize flashcard generator."""
        self.settings = get_settings()
        self.llm = ChatOpenAI(
            model=self.settings.llm_model,
            temperature=0.3,
            openai_api_key=self.settings.openai_api_key
        )
        self._init_prompt()
        logger.info("Initialized flashcard generator")

    def _init_prompt(self) -> None:
        """Initialize generation prompt with improved quality guidelines."""
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """Du bist ein Experte für die Erstellung von Lernkarteikarten nach Spaced-Repetition-Prinzipien.

Erstelle aus dem gegebenen Text Karteikarten, die Studierenden beim Lernen helfen.

**KRITISCHE REGELN (UNBEDINGT BEFOLGEN):**
1. ⚠️  **NIEMALS die Antwort in der Frage verraten!** Die Frage muss beantwortbar sein, OHNE die Antwort zu sehen.
2. Die Frage sollte testendes Wissen abfragen, nicht nur Fakten wiederholen
3. Vermeide Füllwörter wie "laut Text" oder "das Dokument sagt"
4. Keine rhetorischen oder Suggestivfragen

**GUTE vs SCHLECHTE Beispiele:**

❌ SCHLECHT: "Was ist Aktives Zuhören und wie zeigt man Empathie?"
→ Problem: Enthält die Antwort ("Empathie zeigen") bereits in der Frage

✅ GUT: "Welche Techniken gehören zum Aktiven Zuhören?"
→ Antwort: "Paraphrasieren, Nachfragen, Empathie zeigen, Blickkontakt halten"

❌ SCHLECHT: "Erkläre die 4 Phasen des Beratungsgesprächs: Eröffnung, Problemanalyse, Lösungsentwicklung, Abschluss"
→ Problem: Die komplette Antwort steht bereits in der Frage!

✅ GUT: "Nenne die 4 Phasen eines Beratungsgesprächs"
→ Antwort: "1. Eröffnung, 2. Problemanalyse, 3. Lösungsentwicklung, 4. Abschluss"

**Weitere Qualitätsregeln:**
- Fragen sollten präzise und eindeutig sein
- Antworten sollten kurz und prägnant sein (1-3 Sätze)
- Fokussiere auf wichtige Konzepte, Definitionen und Zusammenhänge
- Nutze verschiedene Fragetypen:
  * Definition: "Was ist...?", "Was versteht man unter...?"
  * Aufzählung: "Nenne...", "Welche...gibt es?"
  * Erklärung: "Wie funktioniert...?", "Warum...?"
  * Anwendung: "Wann wird...eingesetzt?", "Wie wendet man...an?"
- Vermeide zu triviale oder zu komplexe Fragen

**Format:** Gib die Karteikarten als JSON-Array zurück:
```json
[
  {{
    "question": "Präzise Frage OHNE Antwort",
    "answer": "Vollständige, prägnante Antwort",
    "difficulty": 1-5,
    "tags": ["tag1", "tag2"]
  }}
]
```

**Schwierigkeitsskala:**
1 = Sehr einfach (Definitionen, Grundlagen)
2 = Einfach (Einfache Konzepte)
3 = Mittel (Standard-Verständnis)
4 = Schwer (Komplexe Zusammenhänge)
5 = Sehr schwer (Tiefes Verständnis, Anwendung)"""),
            ("user", """**Fachgebiet:** {subject}

**Text:**
{text}

**Anzahl Karteikarten:** {count}

Erstelle genau {count} hochwertige Karteikarten. Achte besonders darauf, dass die FRAGE niemals die ANTWORT enthält!""")
        ])

    async def generate_from_documents(
        self,
        documents: List[Document],
        subject: str,
        document_id: str,
        count: int = 10
    ) -> List[str]:
        """
        Generate flashcards from documents.

        Args:
            documents: List of document chunks
            subject: Subject area
            document_id: Source document ID
            count: Number of flashcards to generate

        Returns:
            List of created flashcard IDs
        """
        # Combine relevant chunks
        combined_text = "\n\n".join([
            doc.page_content
            for doc in documents[:10]  # Use first 10 chunks
        ])

        # Truncate if too long
        if len(combined_text) > 8000:
            combined_text = combined_text[:8000] + "..."

        try:
            # Generate flashcards with LLM
            messages = self.prompt.format_messages(
                subject=subject,
                text=combined_text,
                count=min(count, 20)  # Max 20 per batch
            )

            response = self.llm.invoke(messages)

            # Parse JSON response
            flashcards_data = self._parse_flashcards(response.content)

            # Create flashcards in database
            manager = get_flashcard_manager()
            created_ids = []

            for fc in flashcards_data:
                try:
                    card_id = manager.create_flashcard(
                        subject=subject,
                        question=fc["question"],
                        answer=fc["answer"],
                        difficulty=fc.get("difficulty", 3),
                        tags=fc.get("tags", []),
                        document_id=document_id
                    )
                    created_ids.append(card_id)

                except Exception as e:
                    logger.error(f"Error creating flashcard: {str(e)}")

            logger.info(f"Generated {len(created_ids)} flashcards for document {document_id}")
            return created_ids

        except Exception as e:
            logger.error(f"Error generating flashcards: {str(e)}")
            return []

    def _parse_flashcards(self, response: str) -> List[Dict[str, Any]]:
        """
        Parse flashcards from LLM response.

        Args:
            response: LLM response text

        Returns:
            List of flashcard dictionaries
        """
        try:
            # Try to extract JSON from response
            start = response.find("[")
            end = response.rfind("]") + 1

            if start >= 0 and end > start:
                json_str = response[start:end]
                flashcards = json.loads(json_str)

                # Validate structure
                valid_cards = []
                for fc in flashcards:
                    if isinstance(fc, dict) and "question" in fc and "answer" in fc:
                        valid_cards.append(fc)

                return valid_cards

            logger.warning("No valid JSON array found in response")
            return []

        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Error parsing flashcards: {str(e)}")
            return []


# Global generator instance
_generator: FlashcardGenerator | None = None


def get_flashcard_generator() -> FlashcardGenerator:
    """
    Get global flashcard generator instance.

    Returns:
        FlashcardGenerator instance
    """
    global _generator
    if _generator is None:
        _generator = FlashcardGenerator()
    return _generator
