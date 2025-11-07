"""
RAG Chain module for question answering with source citations.
Implements conversation memory and multi-document reasoning.
"""

import logging
import warnings
from typing import Dict, List, Optional, Any

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from app.config import get_settings
from app.services.rag.vector_store import VectorStore

# Suppress LangChain deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="langchain")
# Specifically suppress ConversationBufferMemory deprecation warning
warnings.filterwarnings("ignore", message=".*migrating_memory.*")

logger = logging.getLogger(__name__)


# Custom prompt template for German study assistant
PROMPT_TEMPLATE = """Du bist ein hilfreicher Studienassistent für deutsche Studierende.

Deine Aufgabe ist es, Fragen zu Vorlesungsunterlagen präzise und verständlich zu beantworten.

Wichtige Regeln:
1. Antworte IMMER auf Deutsch
2. Beantworte die Frage basierend auf den gegebenen Kontextdokumenten
3. Gib IMMER die Seitenzahlen als Quelle an (z.B. "Seite 5" oder "Seiten 3-4")
4. Wenn die Antwort nicht in den Dokumenten steht, sage das ehrlich
5. Strukturiere längere Antworten mit Aufzählungen oder Absätzen
6. Verwende Fachbegriffe aus den Dokumenten, erkläre sie aber bei Bedarf

Kontextdokumente:
{context}

Chat-Verlauf:
{chat_history}

Frage: {question}

Hilfreiche Antwort mit Quellenangaben:"""


CONDENSE_QUESTION_TEMPLATE = """Formuliere die Folgefrage so um, dass sie eigenständig verständlich ist.
Verwende den Chat-Verlauf für Kontext, aber erstelle eine vollständige Frage.

Chat-Verlauf:
{chat_history}

Folgefrage: {question}

Eigenständige Frage:"""


class RAGChain:
    """
    Manages the RAG pipeline with conversation memory and citations.
    """

    def __init__(self, vector_store: VectorStore):
        """
        Initialize the RAG chain.

        Args:
            vector_store: VectorStore instance for document retrieval
        """
        self.settings = get_settings()
        self.vector_store = vector_store
        self._llm = None
        self._memory = None
        self._chain = None

    @property
    def llm(self) -> ChatOpenAI:
        """
        Lazy initialization of the LLM.

        Returns:
            ChatOpenAI instance
        """
        if self._llm is None:
            self._llm = ChatOpenAI(
                model=self.settings.llm_model,
                temperature=self.settings.temperature,
                max_tokens=self.settings.max_tokens,
                openai_api_key=self.settings.openai_api_key,
            )
            logger.info(f"Initialized LLM: {self.settings.llm_model}")
        return self._llm

    @property
    def memory(self) -> ConversationBufferMemory:
        """
        Lazy initialization of conversation memory.

        Returns:
            ConversationBufferMemory instance
        """
        if self._memory is None:
            self._memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True,
                output_key="answer",
            )
            logger.info("Initialized conversation memory")
        return self._memory

    def _create_chain(self) -> ConversationalRetrievalChain:
        """
        Create the conversational retrieval chain.

        Returns:
            ConversationalRetrievalChain instance
        """
        # Custom prompts
        qa_prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["context", "chat_history", "question"],
        )

        condense_prompt = PromptTemplate(
            template=CONDENSE_QUESTION_TEMPLATE,
            input_variables=["chat_history", "question"],
        )

        # Get retriever from vector store
        retriever = self.vector_store.get_retriever(
            search_kwargs={"k": self.settings.retrieval_k}
        )

        # Create conversational retrieval chain
        chain = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=retriever,
            memory=self.memory,
            return_source_documents=True,
            combine_docs_chain_kwargs={"prompt": qa_prompt},
            condense_question_prompt=condense_prompt,
            verbose=False,
        )

        logger.info("Created conversational retrieval chain")
        return chain

    @property
    def chain(self) -> ConversationalRetrievalChain:
        """
        Lazy initialization of the RAG chain.

        Returns:
            ConversationalRetrievalChain instance
        """
        if self._chain is None:
            self._chain = self._create_chain()
        return self._chain

    def ask(self, question: str) -> Dict[str, Any]:
        """
        Ask a question and get an answer with sources.

        Args:
            question: User question

        Returns:
            Dictionary with answer, sources, and metadata
        """
        try:
            logger.info(f"Processing question: {question}")

            # Invoke the chain
            result = self.chain.invoke({"question": question})

            # Extract source documents
            source_docs = result.get("source_documents", [])

            # Format sources with page numbers
            sources = self._format_sources(source_docs)

            response = {
                "answer": result["answer"],
                "sources": sources,
                "source_documents": source_docs,
                "question": question,
            }

            logger.info(f"Generated answer with {len(sources)} sources")
            return response

        except Exception as e:
            logger.error(f"Error processing question: {str(e)}")
            raise

    def _format_sources(self, documents: List[Document]) -> List[Dict[str, Any]]:
        """
        Format source documents with page numbers and metadata.

        Args:
            documents: List of source documents

        Returns:
            List of formatted source dictionaries
        """
        sources = []
        seen_sources = set()

        for doc in documents:
            source_file = doc.metadata.get("source_file", "Unknown")
            page = doc.metadata.get("page", "Unknown")

            # Create unique identifier for deduplication
            source_id = f"{source_file}:{page}"

            if source_id not in seen_sources:
                sources.append(
                    {
                        "file": source_file,
                        "page": page + 1 if isinstance(page, int) else page,  # 0-indexed to 1-indexed
                        "content_preview": doc.page_content[:200] + "..."
                        if len(doc.page_content) > 200
                        else doc.page_content,
                    }
                )
                seen_sources.add(source_id)

        return sources

    def clear_memory(self) -> None:
        """Clear the conversation memory."""
        self.memory.clear()
        logger.info("Cleared conversation memory")

    def get_chat_history(self) -> List[Dict[str, str]]:
        """
        Get the current chat history.

        Returns:
            List of chat messages
        """
        messages = self.memory.chat_memory.messages
        history = []

        for msg in messages:
            history.append(
                {
                    "role": "user" if msg.type == "human" else "assistant",
                    "content": msg.content,
                }
            )

        return history

    def reset(self) -> None:
        """Reset the chain and memory."""
        self._chain = None
        self._memory = None
        logger.info("Reset RAG chain and memory")


class RAGAssistant:
    """
    High-level interface for the RAG assistant.
    Combines vector store and RAG chain management.
    """

    def __init__(self):
        """Initialize the RAG assistant."""
        self.vector_store = VectorStore()
        self.rag_chain = RAGChain(self.vector_store)
        logger.info("Initialized RAG Assistant")

    def add_documents(self, documents: List[Document]) -> int:
        """
        Add documents to the knowledge base.

        Args:
            documents: List of documents to add

        Returns:
            Number of documents added
        """
        ids = self.vector_store.add_documents(documents)
        return len(ids)

    def ask(self, question: str) -> Dict[str, Any]:
        """
        Ask a question.

        Args:
            question: User question

        Returns:
            Dictionary with answer and sources
        """
        return self.rag_chain.ask(question)

    def clear_conversation(self) -> None:
        """Clear the conversation history."""
        self.rag_chain.clear_memory()

    def get_stats(self) -> Dict[str, Any]:
        """
        Get system statistics.

        Returns:
            Dictionary with system stats
        """
        collection_stats = self.vector_store.get_collection_stats()
        chat_history = self.rag_chain.get_chat_history()

        return {
            "collection": collection_stats,
            "conversation_length": len(chat_history),
            "model": self.rag_chain.settings.llm_model,
        }

    def delete_document(self, source_file: str) -> None:
        """
        Delete a document from the knowledge base.

        Args:
            source_file: Name of the source file to delete
        """
        self.vector_store.delete_by_source(source_file)

    def get_all_documents(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all documents from the vector store.

        Returns:
            Dictionary with document names and metadata
        """
        return self.vector_store.get_all_documents()


def create_rag_assistant() -> RAGAssistant:
    """
    Factory function to create a RAGAssistant instance.

    Returns:
        RAGAssistant instance
    """
    return RAGAssistant()
