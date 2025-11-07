"""
Document Manager Service
Handles document listing, retrieval, and deletion across all data stores.
"""

import os
import hashlib
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

from loguru import logger
import chromadb

from app.config import get_settings


class DocumentManager:
    """Manages documents across filesystem, ChromaDB, and Neo4j."""

    def __init__(self):
        self.settings = get_settings()
        self.chroma_client = chromadb.PersistentClient(path=str(self.settings.chroma_persist_dir))
        self.collection = self.chroma_client.get_or_create_collection(
            name=self.settings.collection_name
        )

    def _generate_document_id(self, filename: str) -> str:
        """Generate a unique document ID from filename."""
        return hashlib.md5(filename.encode()).hexdigest()[:12]

    def list_documents(
        self,
        subject: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> List[Dict]:
        """
        List all uploaded documents with metadata.

        Args:
            subject: Optional subject filter
            limit: Maximum number of documents
            offset: Number of documents to skip

        Returns:
            List of document info dictionaries
        """
        documents = []
        upload_dir = self.settings.upload_dir

        if not upload_dir.exists():
            return documents

        # Get all PDF files
        pdf_files = list(upload_dir.glob("*.pdf"))

        # Sort by modification time (newest first)
        pdf_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)

        # Apply pagination
        pdf_files = pdf_files[offset:offset + limit]

        for file_path in pdf_files:
            try:
                doc_id = self._generate_document_id(file_path.name)
                file_stats = file_path.stat()

                # Get chunk count from ChromaDB
                chunk_count = 0
                try:
                    results = self.collection.get(
                        where={"document_id": doc_id},
                        include=["metadatas"]
                    )
                    chunk_count = len(results["ids"]) if results["ids"] else 0
                except Exception as e:
                    logger.warning(f"Could not get chunk count for {file_path.name}: {e}")

                doc_info = {
                    "id": doc_id,
                    "filename": file_path.name,
                    "file_size_bytes": file_stats.st_size,
                    "page_count": None,  # Would need PyPDF2 to extract
                    "chunk_count": chunk_count,
                    "uploaded_at": datetime.fromtimestamp(file_stats.st_ctime),
                    "processed": chunk_count > 0,
                    "subject": subject
                }

                # Filter by subject if provided
                if subject is None or doc_info.get("subject") == subject:
                    documents.append(doc_info)

            except Exception as e:
                logger.error(f"Error processing file {file_path}: {e}")
                continue

        return documents

    def get_document(self, document_id: str) -> Optional[Dict]:
        """
        Get details for a specific document.

        Args:
            document_id: Document ID

        Returns:
            Document info dictionary or None
        """
        upload_dir = self.settings.upload_dir

        # Find file with matching document_id
        for file_path in upload_dir.glob("*.pdf"):
            if self._generate_document_id(file_path.name) == document_id:
                file_stats = file_path.stat()

                # Get chunk count
                chunk_count = 0
                try:
                    results = self.collection.get(
                        where={"document_id": document_id},
                        include=["metadatas"]
                    )
                    chunk_count = len(results["ids"]) if results["ids"] else 0
                except Exception as e:
                    logger.warning(f"Could not get chunk count: {e}")

                return {
                    "id": document_id,
                    "filename": file_path.name,
                    "file_size_bytes": file_stats.st_size,
                    "page_count": None,
                    "chunk_count": chunk_count,
                    "uploaded_at": datetime.fromtimestamp(file_stats.st_ctime),
                    "processed": chunk_count > 0,
                    "subject": None
                }

        return None

    def delete_document(
        self,
        document_id: str,
        delete_from_graph: bool = True,
        delete_flashcards: bool = True
    ) -> Dict[str, any]:
        """
        Delete a document and all associated data.

        Args:
            document_id: Document ID
            delete_from_graph: Whether to delete from Neo4j
            delete_flashcards: Whether to delete associated flashcards

        Returns:
            Dictionary with deletion results
        """
        results = {
            "document_id": document_id,
            "file_deleted": False,
            "chunks_deleted": 0,
            "graph_cleared": False,
            "flashcards_deleted": 0,
            "errors": []
        }

        # 1. Delete physical file
        upload_dir = self.settings.upload_dir
        file_path = None

        for pdf_file in upload_dir.glob("*.pdf"):
            if self._generate_document_id(pdf_file.name) == document_id:
                file_path = pdf_file
                break

        if file_path and file_path.exists():
            try:
                file_path.unlink()
                results["file_deleted"] = True
                logger.info(f"Deleted file: {file_path}")
            except Exception as e:
                error_msg = f"Failed to delete file: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)

        # 2. Delete from ChromaDB
        try:
            # Get all chunks for this document
            doc_results = self.collection.get(
                where={"document_id": document_id},
                include=["documents"]
            )

            if doc_results["ids"]:
                self.collection.delete(ids=doc_results["ids"])
                results["chunks_deleted"] = len(doc_results["ids"])
                logger.info(f"Deleted {len(doc_results['ids'])} chunks from ChromaDB")
        except Exception as e:
            error_msg = f"Failed to delete from ChromaDB: {str(e)}"
            results["errors"].append(error_msg)
            logger.error(error_msg)

        # 3. Delete from Neo4j (if requested)
        if delete_from_graph:
            try:
                from app.services.graph.graph_builder import get_graph_builder
                graph_builder = get_graph_builder()

                # Delete all nodes/relationships for this document
                deletion_result = graph_builder.delete_by_document(document_id)
                results["graph_cleared"] = True
                results["graph_nodes_deleted"] = deletion_result["nodes_deleted"]
                logger.info(f"Cleared graph data for document {document_id}: {deletion_result}")
            except Exception as e:
                error_msg = f"Failed to delete from graph: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)

        # 4. Delete associated flashcards (if requested)
        if delete_flashcards:
            try:
                from app.services.flashcards.flashcard_manager import get_flashcard_manager
                manager = get_flashcard_manager()

                # Delete flashcards with this document_id
                count = manager.delete_flashcards_by_document(document_id)
                results["flashcards_deleted"] = count
                logger.info(f"Deleted {count} flashcards for document {document_id}")
            except Exception as e:
                error_msg = f"Failed to delete flashcards: {str(e)}"
                results["errors"].append(error_msg)
                logger.error(error_msg)

        return results

    def clear_all_documents(self) -> Dict[str, any]:
        """
        Clear ALL documents and data (use with caution!).

        Returns:
            Dictionary with clearing results
        """
        results = {
            "files_deleted": 0,
            "chunks_deleted": 0,
            "errors": []
        }

        # Delete all files
        upload_dir = self.settings.upload_dir
        for pdf_file in upload_dir.glob("*.pdf"):
            try:
                pdf_file.unlink()
                results["files_deleted"] += 1
            except Exception as e:
                results["errors"].append(f"Failed to delete {pdf_file.name}: {e}")

        # Clear ChromaDB collection
        try:
            self.chroma_client.delete_collection(name=self.settings.chroma_collection_name)
            self.collection = self.chroma_client.get_or_create_collection(
                name=self.settings.chroma_collection_name
            )
            logger.info("Cleared ChromaDB collection")
        except Exception as e:
            results["errors"].append(f"Failed to clear ChromaDB: {e}")

        return results


# Singleton instance
_document_manager: Optional[DocumentManager] = None


def get_document_manager() -> DocumentManager:
    """Get or create document manager instance."""
    global _document_manager
    if _document_manager is None:
        _document_manager = DocumentManager()
    return _document_manager
