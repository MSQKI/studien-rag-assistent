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
from app.services.rag.advanced_document_processor import AdvancedDocumentProcessor
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

        # Choose PDF processor based on config
        if self.settings.use_advanced_pdf_processing:
            try:
                self.doc_processor = AdvancedDocumentProcessor()
                logger.info("✅ Using Advanced PDF Processor (Unstructured.io)")
            except Exception as e:
                logger.warning(f"Advanced processor unavailable ({e}), falling back to standard")
                self.doc_processor = DocumentProcessor()
        else:
            self.doc_processor = DocumentProcessor()
            logger.info("Using Standard PDF Processor (PyPDF)")

        self.entity_extractor = EntityExtractor()
        self.flashcard_generator = FlashcardGenerator()
        logger.info("Initialized document pipeline")

    async def process_document(
        self,
        file_path: Path,
        subject: str | None = None,
        assistant: RAGAssistant = None,
        graph_builder: GraphBuilder = None,
        document_id: str | None = None
    ) -> Dict[str, Any]:
        """
        Process a document through the complete pipeline with parallel processing.

        Args:
            file_path: Path to PDF file
            subject: Optional subject classification
            assistant: RAG assistant instance
            graph_builder: Graph builder instance
            document_id: Optional document ID (generated if not provided)

        Returns:
            Processing results with statistics
        """
        import asyncio

        if document_id is None:
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
            # Step 1: Extract and chunk document (must happen first)
            logger.info(f"Step 1/4: Chunking document {filename}")

            # Use appropriate processor (async for advanced, sync for standard)
            if isinstance(self.doc_processor, AdvancedDocumentProcessor):
                documents = await self.doc_processor.process_pdf(
                    file_path,
                    use_vision=self.settings.use_vision_for_images
                )
            else:
                documents = self.doc_processor.process_pdf(file_path)

            # Add document_id to ALL chunk metadata for tracking
            for doc in documents:
                doc.metadata["document_id"] = document_id
                doc.metadata["filename"] = filename

            results["chunks_created"] = len(documents)

            logger.info(f"Created {len(documents)} chunks (advanced={self.settings.use_advanced_pdf_processing}, vision={self.settings.use_vision_for_images}), now processing in parallel...")

            # Step 2-4: Process in parallel for speed
            tasks = []

            # Task 1: Add to vector store (RAG)
            async def add_to_vector_store():
                if assistant:
                    logger.info(f"Adding {len(documents)} chunks to vector store")
                    try:
                        # Process in batches for better performance
                        batch_size = 50
                        for i in range(0, len(documents), batch_size):
                            batch = documents[i:i+batch_size]
                            assistant.add_documents(batch)
                            logger.info(f"Processed batch {i//batch_size + 1}/{(len(documents) + batch_size - 1)//batch_size}")
                    except Exception as e:
                        logger.error(f"Error adding to vector store: {str(e)}")
                        results["errors"].append(f"Vector store: {str(e)}")

            # Task 2: Entity extraction for knowledge graph
            async def extract_entities():
                if graph_builder and self.settings.entity_extraction_enabled:
                    logger.info(f"Extracting entities for knowledge graph")
                    try:
                        # Smart sampling: first chunks + evenly distributed samples
                        sample_size = min(30, len(documents))  # Reduced from 50
                        if len(documents) > sample_size:
                            # Take first 10 chunks + evenly distributed samples
                            step = len(documents) // (sample_size - 10)
                            sampled_docs = documents[:10] + [documents[i] for i in range(10, len(documents), step)][:sample_size-10]
                        else:
                            sampled_docs = documents

                        chunks_for_extraction = [
                            {
                                "text": doc.page_content,
                                "metadata": doc.metadata
                            }
                            for doc in sampled_docs
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

            # Task 3: Generate flashcards
            async def generate_flashcards():
                if self.settings.flashcard_generation_enabled:
                    logger.info(f"Generating flashcards")
                    try:
                        # Smart sampling for flashcards
                        sample_size = min(15, len(documents))  # Reduced from 20
                        if len(documents) > sample_size:
                            # Take chunks from beginning, middle, end
                            third = len(documents) // 3
                            sampled_docs = documents[:5] + documents[third:third+5] + documents[-5:]
                        else:
                            sampled_docs = documents[:sample_size]

                        flashcards = await self.flashcard_generator.generate_from_documents(
                            documents=sampled_docs,
                            subject=subject or "General",
                            document_id=document_id,
                            count=self.settings.flashcards_per_document
                        )
                        results["flashcards_generated"] = len(flashcards)

                    except Exception as e:
                        logger.error(f"Error generating flashcards: {str(e)}")
                        results["errors"].append(f"Flashcard generation: {str(e)}")

            # Run all tasks in parallel
            await asyncio.gather(
                add_to_vector_store(),
                extract_entities(),
                generate_flashcards(),
                return_exceptions=True  # Don't fail all if one task fails
            )

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
