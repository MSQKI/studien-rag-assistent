"""
Document processing module for PDF handling and text chunking.
Supports batch processing and metadata extraction.
"""

import logging
from pathlib import Path
from typing import List, Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document

from src.config import get_settings

logger = logging.getLogger(__name__)


class DocumentProcessor:
    """
    Handles PDF document loading, processing, and chunking.
    """

    def __init__(self):
        """Initialize the document processor with settings."""
        self.settings = get_settings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
            is_separator_regex=False,
        )

    def load_pdf(self, file_path: Path) -> List[Document]:
        """
        Load a PDF file and extract its content.

        Args:
            file_path: Path to the PDF file

        Returns:
            List of Document objects with page content and metadata

        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            Exception: If PDF loading fails
        """
        if not file_path.exists():
            raise FileNotFoundError(f"PDF file not found: {file_path}")

        try:
            logger.info(f"Loading PDF: {file_path}")
            loader = PyPDFLoader(str(file_path))
            documents = loader.load()

            # Enrich metadata
            for doc in documents:
                doc.metadata["source_file"] = file_path.name
                doc.metadata["file_path"] = str(file_path)

            logger.info(f"Successfully loaded {len(documents)} pages from {file_path.name}")
            return documents

        except Exception as e:
            logger.error(f"Error loading PDF {file_path}: {str(e)}")
            raise

    def split_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into smaller chunks for embedding.

        Args:
            documents: List of documents to split

        Returns:
            List of chunked documents with preserved metadata
        """
        try:
            logger.info(f"Splitting {len(documents)} documents into chunks")
            chunks = self.text_splitter.split_documents(documents)

            # Add chunk metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata["chunk_id"] = i
                chunk.metadata["chunk_size"] = len(chunk.page_content)

            logger.info(f"Created {len(chunks)} chunks from {len(documents)} documents")
            return chunks

        except Exception as e:
            logger.error(f"Error splitting documents: {str(e)}")
            raise

    def process_pdf(self, file_path: Path) -> List[Document]:
        """
        Complete processing pipeline: load PDF and split into chunks.

        Args:
            file_path: Path to the PDF file

        Returns:
            List of processed and chunked documents

        Raises:
            FileNotFoundError: If the PDF file doesn't exist
            Exception: If processing fails
        """
        try:
            # Load PDF
            documents = self.load_pdf(file_path)

            # Split into chunks
            chunks = self.split_documents(documents)

            logger.info(
                f"Processed {file_path.name}: {len(documents)} pages → {len(chunks)} chunks"
            )
            return chunks

        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            raise

    def process_multiple_pdfs(
        self, file_paths: List[Path], batch_size: Optional[int] = None
    ) -> List[Document]:
        """
        Process multiple PDF files in batches.

        Args:
            file_paths: List of PDF file paths
            batch_size: Number of files to process per batch (default: from settings)

        Returns:
            Combined list of all processed documents

        Raises:
            Exception: If batch processing fails
        """
        if batch_size is None:
            batch_size = self.settings.batch_size

        all_chunks = []
        total_files = len(file_paths)

        logger.info(f"Processing {total_files} PDF files in batches of {batch_size}")

        for i in range(0, total_files, batch_size):
            batch = file_paths[i : i + batch_size]
            batch_num = i // batch_size + 1
            total_batches = (total_files + batch_size - 1) // batch_size

            logger.info(f"Processing batch {batch_num}/{total_batches}")

            for file_path in batch:
                try:
                    chunks = self.process_pdf(file_path)
                    all_chunks.extend(chunks)
                except Exception as e:
                    logger.error(f"Failed to process {file_path}: {str(e)}")
                    # Continue with next file instead of failing completely
                    continue

        logger.info(
            f"Completed processing {total_files} files → {len(all_chunks)} total chunks"
        )
        return all_chunks

    def get_document_stats(self, documents: List[Document]) -> dict:
        """
        Calculate statistics for processed documents.

        Args:
            documents: List of documents

        Returns:
            Dictionary with document statistics
        """
        if not documents:
            return {
                "total_chunks": 0,
                "total_characters": 0,
                "avg_chunk_size": 0,
                "unique_sources": 0,
            }

        total_chars = sum(len(doc.page_content) for doc in documents)
        unique_sources = len(set(doc.metadata.get("source_file") for doc in documents))

        return {
            "total_chunks": len(documents),
            "total_characters": total_chars,
            "avg_chunk_size": total_chars // len(documents),
            "unique_sources": unique_sources,
        }


def validate_pdf(file_path: Path) -> bool:
    """
    Validate if a file is a valid PDF.

    Args:
        file_path: Path to the file

    Returns:
        True if valid PDF, False otherwise
    """
    if not file_path.exists():
        return False

    if file_path.suffix.lower() != ".pdf":
        return False

    # Basic PDF signature check
    try:
        with open(file_path, "rb") as f:
            header = f.read(4)
            return header == b"%PDF"
    except Exception:
        return False
