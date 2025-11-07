"""
Vector store module for document embeddings and similarity search.
Integrates ChromaDB with OpenAI embeddings.
"""

import logging
import os
from pathlib import Path
from typing import List, Optional, Dict, Any

from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings

from app.config import get_settings
from app.services.shared_chroma import get_chroma_client

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Manages document embeddings and vector similarity search using ChromaDB.
    """

    def __init__(self):
        """Initialize the vector store with OpenAI embeddings and ChromaDB."""
        self.settings = get_settings()
        self._embeddings = None
        self._vectorstore = None
        self._chroma_client = None

    @property
    def embeddings(self) -> OpenAIEmbeddings:
        """
        Lazy initialization of OpenAI embeddings.

        Returns:
            OpenAIEmbeddings instance
        """
        if self._embeddings is None:
            self._embeddings = OpenAIEmbeddings(
                model=self.settings.embedding_model,
                openai_api_key=self.settings.openai_api_key,
            )
            logger.info(f"Initialized OpenAI embeddings with model: {self.settings.embedding_model}")
        return self._embeddings

    @property
    def chroma_client(self):
        """
        Get the shared ChromaDB persistent client.

        Returns:
            ChromaDB PersistentClient instance
        """
        if self._chroma_client is None:
            # Use shared client to avoid multiple instances
            self._chroma_client = get_chroma_client()
            logger.info(f"Using shared ChromaDB client at: {self.settings.chroma_persist_dir}")
        return self._chroma_client

    @property
    def vectorstore(self) -> Chroma:
        """
        Lazy initialization of ChromaDB vector store.

        Returns:
            Chroma vector store instance
        """
        if self._vectorstore is None:
            self._vectorstore = Chroma(
                client=self.chroma_client,
                collection_name=self.settings.collection_name,
                embedding_function=self.embeddings,
            )
            logger.info(f"Initialized Chroma vectorstore with collection: {self.settings.collection_name}")
        return self._vectorstore

    def add_documents(self, documents: List[Document]) -> List[str]:
        """
        Add documents to the vector store.

        Args:
            documents: List of documents to add

        Returns:
            List of document IDs

        Raises:
            Exception: If adding documents fails
        """
        try:
            logger.info(f"Adding {len(documents)} documents to vector store")
            ids = self.vectorstore.add_documents(documents)
            logger.info(f"Successfully added {len(ids)} documents")
            return ids

        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise

    def similarity_search(
        self,
        query: str,
        k: Optional[int] = None,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """
        Perform similarity search for a query.

        Args:
            query: Search query
            k: Number of results to return (default: from settings)
            filter: Metadata filter dictionary

        Returns:
            List of most similar documents
        """
        if k is None:
            k = self.settings.retrieval_k

        try:
            logger.info(f"Performing similarity search for: '{query}' (k={k})")
            results = self.vectorstore.similarity_search(
                query=query,
                k=k,
                filter=filter,
            )
            logger.info(f"Found {len(results)} similar documents")
            return results

        except Exception as e:
            logger.error(f"Error during similarity search: {str(e)}")
            raise

    def similarity_search_with_score(
        self,
        query: str,
        k: Optional[int] = None,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[tuple[Document, float]]:
        """
        Perform similarity search with relevance scores.

        Args:
            query: Search query
            k: Number of results to return (default: from settings)
            filter: Metadata filter dictionary

        Returns:
            List of tuples (document, score)
        """
        if k is None:
            k = self.settings.retrieval_k

        try:
            logger.info(f"Performing similarity search with scores for: '{query}' (k={k})")
            results = self.vectorstore.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter,
            )
            logger.info(f"Found {len(results)} documents with scores")
            return results

        except Exception as e:
            logger.error(f"Error during similarity search with scores: {str(e)}")
            raise

    def get_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """
        Get a retriever for RAG chains.

        Args:
            search_kwargs: Additional search parameters

        Returns:
            VectorStoreRetriever instance
        """
        if search_kwargs is None:
            search_kwargs = {"k": self.settings.retrieval_k}

        return self.vectorstore.as_retriever(search_kwargs=search_kwargs)

    def delete_collection(self) -> None:
        """
        Delete the entire collection (use with caution!).
        """
        try:
            logger.warning(f"Deleting collection: {self.settings.collection_name}")
            self.vectorstore.delete_collection()
            self._vectorstore = None  # Reset to force reinitialization
            logger.info("Collection deleted successfully")

        except Exception as e:
            logger.error(f"Error deleting collection: {str(e)}")
            raise

    def get_collection_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the current collection.

        Returns:
            Dictionary with collection statistics
        """
        try:
            collection = self.vectorstore._collection
            count = collection.count()

            return {
                "collection_name": self.settings.collection_name,
                "document_count": count,
                "persist_directory": str(self.settings.chroma_persist_dir),
            }

        except Exception as e:
            logger.error(f"Error getting collection stats: {str(e)}")
            return {
                "collection_name": self.settings.collection_name,
                "document_count": 0,
                "error": str(e),
            }

    def delete_by_source(self, source_file: str) -> None:
        """
        Delete all documents from a specific source file.

        Args:
            source_file: Name of the source file
        """
        try:
            logger.info(f"Deleting documents from source: {source_file}")

            # Get the ChromaDB collection
            collection = self.vectorstore._collection

            # Get all documents with the matching source_file
            results = collection.get(
                where={"source_file": source_file}
            )

            if results and results['ids']:
                # Delete by IDs
                collection.delete(ids=results['ids'])
                logger.info(f"Deleted {len(results['ids'])} documents from {source_file}")
            else:
                logger.info(f"No documents found for source: {source_file}")

        except Exception as e:
            logger.error(f"Error deleting documents by source: {str(e)}")
            raise

    def document_exists(self, source_file: str) -> bool:
        """
        Check if documents from a specific source already exist.

        Args:
            source_file: Name of the source file

        Returns:
            True if documents exist, False otherwise
        """
        try:
            results = self.vectorstore.similarity_search(
                query="",  # Empty query
                k=1,
                filter={"source_file": source_file},
            )
            return len(results) > 0

        except Exception:
            return False

    def get_all_documents(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all unique documents from the vector store with metadata.

        Returns:
            Dictionary with source files as keys and metadata as values
            Format: {"filename.pdf": {"chunk_count": 5, "pages": [1,2,3]}}
        """
        try:
            collection = self.vectorstore._collection

            # Get all items from collection
            results = collection.get(
                include=["metadatas"]
            )

            if not results or not results.get("metadatas"):
                return {}

            # Aggregate by source file
            documents = {}
            for metadata in results["metadatas"]:
                if metadata and "source_file" in metadata:
                    source_file = metadata["source_file"]

                    if source_file not in documents:
                        documents[source_file] = {
                            "chunk_count": 0,
                            "pages": set()
                        }

                    documents[source_file]["chunk_count"] += 1

                    if "page" in metadata:
                        documents[source_file]["pages"].add(metadata["page"])

            # Convert page sets to sorted lists
            for doc in documents.values():
                doc["pages"] = sorted(list(doc["pages"]))

            logger.info(f"Found {len(documents)} unique documents in vector store")
            return documents

        except Exception as e:
            logger.error(f"Error getting all documents: {str(e)}")
            return {}


def create_vector_store() -> VectorStore:
    """
    Factory function to create a VectorStore instance.

    Returns:
        VectorStore instance
    """
    return VectorStore()
