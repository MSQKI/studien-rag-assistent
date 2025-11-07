"""
Document Processing Pipeline
Orchestrates document processing across all services.
"""

import uuid
from pathlib import Path
from typing import Dict, Any, List

from loguru import logger

from app.config import get_settings
from app.services.rag.document_processor import DocumentProcessor
from app.services.rag.rag_chain import RAGAssistant
from app.services.graph.entity_extractor import EntityExtractor
from app.services.graph.graph_builder import GraphBuilder
from app.services.flashcards.flashcard_generator import FlashcardGenerator


class DocumentPipeline:
    """
    Orchestrates document processing pipeline:
    1. Save PDF
    2. Extract text and chunk
    3. Add to vector store (RAG)
    4. Extract entities for graph
    5. Generate flashcards
    """

    def __init__(self):
        """Initialize pipeline components."""
        self.settings = get_settings()
        self.doc_processor = DocumentProcessor()
        self.entity_extractor = EntityExtractor()
        self.flashcard_generator = FlashcardGenerator()
        logger.info("Initialized document pipeline")

    async def process_document(
        self,
        file_path: Path,
        subject: str | None = None,
        assistant: RAGAssistant = None,
        graph_builder: GraphBuilder = None
    ) -> Dict[str, Any]:
        """
        Process a document through the complete pipeline.

        Args:
            file_path: Path to PDF file
            subject: Optional subject classification
            assistant: RAG assistant instance
            graph_builder: Graph builder instance

        Returns:
            Processing results with statistics
        """
        document_id = str(uuid.uuid4())
        filename = file_path.name

        logger.info(f"Processing document: {filename} (ID: {document_id})")

        results = {
            "document_id": document_id,
            "filename": filename,
            "subject": subject,
            "chunks_created": 0,
            "entities_extracted": 0,
            "relationships_created": 0,
            "flashcards_generated": 0,
            "errors": []
        }

        try:
            # Step 1: Extract and chunk document
            logger.info(f"Step 1/4: Chunking document {filename}")
            documents = self.doc_processor.process_pdf(file_path)
            results["chunks_created"] = len(documents)

            # Step 2: Add to vector store (RAG)
            if assistant:
                logger.info(f"Step 2/4: Adding {len(documents)} chunks to vector store")
                try:
                    assistant.add_documents(documents)
                except Exception as e:
                    logger.error(f"Error adding to vector store: {str(e)}")
                    results["errors"].append(f"Vector store: {str(e)}")

            # Step 3: Entity extraction for knowledge graph
            if graph_builder and self.settings.entity_extraction_enabled:
                logger.info(f"Step 3/4: Extracting entities for knowledge graph")
                try:
                    # Prepare chunks for extraction
                    chunks_for_extraction = [
                        {
                            "text": doc.page_content,
                            "metadata": doc.metadata
                        }
                        for doc in documents[:50]  # Limit to first 50 chunks
                    ]

                    graph_data = self.entity_extractor.extract_from_document_chunks(
                        chunks_for_extraction,
                        subject=subject
                    )

                    # Add to graph
                    graph_result = graph_builder.add_graph_data(graph_data)
                    results["entities_extracted"] = graph_result["nodes_created"]
                    results["relationships_created"] = graph_result["relationships_created"]

                except Exception as e:
                    logger.error(f"Error in entity extraction: {str(e)}")
                    results["errors"].append(f"Entity extraction: {str(e)}")

            # Step 4: Generate flashcards
            if self.settings.flashcard_generation_enabled:
                logger.info(f"Step 4/4: Generating flashcards")
                try:
                    flashcards = await self.flashcard_generator.generate_from_documents(
                        documents=documents[:20],  # First 20 chunks
                        subject=subject or "General",
                        document_id=document_id,
                        count=self.settings.flashcards_per_document
                    )
                    results["flashcards_generated"] = len(flashcards)

                except Exception as e:
                    logger.error(f"Error generating flashcards: {str(e)}")
                    results["errors"].append(f"Flashcard generation: {str(e)}")

            logger.info(f"Document processing complete: {filename}")
            return results

        except Exception as e:
            logger.error(f"Critical error in document pipeline: {str(e)}")
            results["errors"].append(f"Critical: {str(e)}")
            raise


# Global pipeline instance
_pipeline: DocumentPipeline | None = None


def get_document_pipeline() -> DocumentPipeline:
    """
    Get global document pipeline instance.

    Returns:
        DocumentPipeline instance
    """
    global _pipeline
    if _pipeline is None:
        _pipeline = DocumentPipeline()
    return _pipeline
