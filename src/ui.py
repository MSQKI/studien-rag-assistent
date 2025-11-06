"""
Streamlit UI for the RAG Study Assistant.
Provides file upload, chat interface, and source citations.
"""

import os
import sys
from pathlib import Path

# Disable ChromaDB telemetry BEFORE any imports
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import logging
from typing import List, Dict, Any
import json

import streamlit as st
from loguru import logger as loguru_logger

from src.config import get_settings
from src.document_processor import DocumentProcessor, validate_pdf
from src.rag_chain import create_rag_assistant

# Configure logging
logging.basicConfig(level=logging.INFO)


def setup_page():
    """Configure Streamlit page settings."""
    st.set_page_config(
        page_title="Studien-RAG-Assistent",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Custom CSS
    st.markdown(
        """
        <style>
        .stChatMessage {
            background-color: #f0f2f6;
            border-radius: 10px;
            padding: 10px;
            margin: 5px 0;
        }
        .source-box {
            background-color: #e8f4f8;
            border-left: 3px solid #1f77b4;
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
        }
        .stats-box {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "assistant" not in st.session_state:
        st.session_state.assistant = create_rag_assistant()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []

    if "processor" not in st.session_state:
        st.session_state.processor = DocumentProcessor()

    if "settings" not in st.session_state:
        st.session_state.settings = get_settings()

    if "confirm_reset" not in st.session_state:
        st.session_state.confirm_reset = False


def render_sidebar():
    """Render the sidebar with file upload and management."""
    with st.sidebar:
        st.title("📚 Studien-RAG-Assistent")
        st.markdown("---")

        # File Upload Section
        st.header("📄 Dokumente hochladen")

        uploaded_files = st.file_uploader(
            "PDF-Dateien auswählen",
            type=["pdf"],
            accept_multiple_files=True,
            help="Wähle eine oder mehrere PDF-Dateien aus deinen Vorlesungsunterlagen",
        )

        if uploaded_files:
            if st.button("📤 Dokumente verarbeiten", type="primary"):
                process_uploaded_files(uploaded_files)

        st.markdown("---")

        # Document Management
        st.header("📋 Dokumente in der Datenbank")

        # Get all documents from vector store (not just session)
        all_docs = st.session_state.assistant.get_all_documents()

        if all_docs:
            st.caption(f"Insgesamt {len(all_docs)} Dokument(e)")

            for file_name, metadata in all_docs.items():
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.text(f"📄 {file_name}")
                        st.caption(
                            f"📚 {metadata['chunk_count']} Chunks | "
                            f"📖 Seiten: {', '.join(map(str, metadata['pages'][:5]))}"
                            f"{'...' if len(metadata['pages']) > 5 else ''}"
                        )
                    with col2:
                        if st.button("🗑️", key=f"delete_{file_name}", help=f"{file_name} löschen"):
                            delete_document(file_name)

                    st.markdown("---")
        else:
            st.info("Noch keine Dokumente in der Datenbank")

        st.markdown("---")

        # Statistics
        st.header("📊 Statistiken")
        render_statistics()

        st.markdown("---")

        # Settings & Actions
        st.header("⚙️ Aktionen")

        if st.button("🗑️ Konversation löschen"):
            clear_conversation()

        # Reset All mit Bestätigung
        if st.session_state.confirm_reset:
            st.warning("⚠️ Wirklich ALLES löschen?\n\n(Dokumente + Konversation)")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Ja", type="primary"):
                    reset_all()
            with col2:
                if st.button("❌ Abbrechen"):
                    st.session_state.confirm_reset = False
                    st.rerun()
        else:
            if st.button("🔄 Alles zurücksetzen", type="secondary"):
                reset_all()


def process_uploaded_files(uploaded_files: List) -> None:
    """
    Process uploaded PDF files.

    Args:
        uploaded_files: List of uploaded file objects from Streamlit
    """
    settings = st.session_state.settings
    processor = st.session_state.processor
    assistant = st.session_state.assistant

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()

    total_files = len(uploaded_files)
    processed_files = []

    for i, uploaded_file in enumerate(uploaded_files):
        try:
            # Update progress
            progress = (i + 1) / total_files
            progress_bar.progress(progress)
            status_text.text(f"Verarbeite: {uploaded_file.name} ({i+1}/{total_files})")

            # Save uploaded file
            file_path = settings.upload_dir / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Validate PDF
            if not validate_pdf(file_path):
                st.sidebar.error(f"❌ {uploaded_file.name} ist keine gültige PDF-Datei")
                file_path.unlink()  # Delete invalid file
                continue

            # Check if already processed
            if assistant.vector_store.document_exists(uploaded_file.name):
                st.sidebar.warning(f"⚠️ {uploaded_file.name} wurde bereits verarbeitet")
                continue

            # Process PDF
            documents = processor.process_pdf(file_path)

            # Add to vector store
            assistant.add_documents(documents)

            processed_files.append(uploaded_file.name)
            st.sidebar.success(f"✅ {uploaded_file.name} erfolgreich verarbeitet")

        except Exception as e:
            st.sidebar.error(f"❌ Fehler bei {uploaded_file.name}: {str(e)}")
            loguru_logger.error(f"Error processing {uploaded_file.name}: {str(e)}")

    # Update session state
    st.session_state.uploaded_files.extend(processed_files)

    # Clear progress
    progress_bar.empty()
    status_text.empty()

    if processed_files:
        st.sidebar.success(f"✅ {len(processed_files)} Dokument(e) erfolgreich hinzugefügt!")
    else:
        st.sidebar.info("Keine neuen Dokumente hinzugefügt")


def delete_document(file_name: str) -> None:
    """
    Delete a document from the knowledge base.

    Args:
        file_name: Name of the file to delete
    """
    try:
        assistant = st.session_state.assistant

        # Delete from vector store (ChromaDB)
        assistant.delete_document(file_name)
        loguru_logger.info(f"Deleted document from vector store: {file_name}")

        # Remove from uploaded files list (if it's there)
        if file_name in st.session_state.uploaded_files:
            st.session_state.uploaded_files.remove(file_name)

        # Delete physical file if exists
        file_path = st.session_state.settings.upload_dir / file_name
        if file_path.exists():
            file_path.unlink()
            loguru_logger.info(f"Deleted physical file: {file_path}")

        st.sidebar.success(f"✅ {file_name} wurde gelöscht")
        st.rerun()

    except Exception as e:
        st.sidebar.error(f"❌ Fehler beim Löschen: {str(e)}")
        loguru_logger.error(f"Error deleting {file_name}: {str(e)}")


def clear_conversation() -> None:
    """Clear the conversation history."""
    st.session_state.assistant.clear_conversation()
    st.session_state.chat_history = []
    st.sidebar.success("✅ Konversation gelöscht")
    st.rerun()


def reset_all() -> None:
    """Reset all data including documents and conversation."""
    # Zwei-Stufen-Bestätigung
    if not st.session_state.confirm_reset:
        # Erste Stufe: Warnung anzeigen
        st.session_state.confirm_reset = True
        st.rerun()
    else:
        # Zweite Stufe: Wirklich ausführen
        try:
            st.session_state.assistant.vector_store.delete_collection()
            st.session_state.chat_history = []
            st.session_state.uploaded_files = []
            st.session_state.confirm_reset = False

            # Reinitialize assistant with fresh vector store
            st.session_state.assistant = create_rag_assistant()

            st.sidebar.success("✅ Alles wurde zurückgesetzt")
            st.rerun()
        except Exception as e:
            st.sidebar.error(f"❌ Fehler beim Zurücksetzen: {str(e)}")
            st.session_state.confirm_reset = False


def render_statistics() -> None:
    """Render system statistics."""
    try:
        # Get fresh stats from vector store
        stats = st.session_state.assistant.get_stats()
        all_docs = st.session_state.assistant.get_all_documents()

        # Count actual files in vector store
        num_files = len(all_docs)
        num_chunks = stats["collection"]["document_count"]

        st.metric("📄 PDFs", num_files)
        st.metric("📚 Text-Chunks", num_chunks)
        st.metric("💬 Nachrichten", stats["conversation_length"])

        # Zusätzliche Info
        if num_chunks > 0 and num_files > 0:
            avg_chunks = num_chunks // num_files if num_files > 0 else 0
            st.caption(f"∅ {avg_chunks} Chunks pro PDF")
        elif num_chunks == 0 and num_files == 0:
            st.caption("Keine Dokumente geladen")

        st.caption(f"🤖 {stats['model']}")

    except Exception as e:
        st.error(f"Fehler beim Laden der Statistiken: {str(e)}")
        loguru_logger.error(f"Statistics error: {str(e)}")


def render_chat_interface():
    """Render the main chat interface."""
    st.title("💬 Chat mit deinen Vorlesungsunterlagen")

    # Display chat history
    for message in st.session_state.chat_history:
        render_message(message)

    # Chat input
    if prompt := st.chat_input("Stelle eine Frage zu deinen Unterlagen..."):
        # Add user message
        user_message = {"role": "user", "content": prompt}
        st.session_state.chat_history.append(user_message)

        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Denke nach..."):
                try:
                    response = st.session_state.assistant.ask(prompt)

                    # Display answer
                    st.write(response["answer"])

                    # Display sources
                    if response["sources"]:
                        with st.expander("📚 Quellenangaben", expanded=True):
                            render_sources(response["sources"])

                    # Add assistant message to history
                    assistant_message = {
                        "role": "assistant",
                        "content": response["answer"],
                        "sources": response["sources"],
                    }
                    st.session_state.chat_history.append(assistant_message)

                except Exception as e:
                    st.error(f"❌ Fehler bei der Antwortgenerierung: {str(e)}")
                    loguru_logger.error(f"Error generating response: {str(e)}")


def render_message(message: Dict[str, Any]) -> None:
    """
    Render a single chat message.

    Args:
        message: Message dictionary with role and content
    """
    with st.chat_message(message["role"]):
        st.write(message["content"])

        # Render sources if available
        if message["role"] == "assistant" and "sources" in message:
            if message["sources"]:
                with st.expander("📚 Quellenangaben"):
                    render_sources(message["sources"])


def render_sources(sources: List[Dict[str, Any]]) -> None:
    """
    Render source citations.

    Args:
        sources: List of source dictionaries
    """
    for i, source in enumerate(sources, 1):
        st.markdown(
            f"""
            <div class="source-box">
                <strong>Quelle {i}:</strong> {source['file']}, Seite {source['page']}<br>
                <em>{source['content_preview']}</em>
            </div>
            """,
            unsafe_allow_html=True,
        )


def main():
    """Main application entry point."""
    setup_page()
    initialize_session_state()

    # Render UI
    render_sidebar()

    # Check if any documents exist in the database
    all_docs = st.session_state.assistant.get_all_documents()

    # Main content
    if not all_docs:
        st.info("👈 Lade zunächst PDF-Dokumente in der Seitenleiste hoch")
        st.markdown(
            """
            ### Willkommen beim Studien-RAG-Assistenten! 🎓

            Dieser Assistent hilft dir dabei, deine Vorlesungsunterlagen intelligent zu durchsuchen und Fragen zu beantworten.

            **So funktioniert's:**
            1. Lade deine PDF-Dokumente in der Seitenleiste hoch
            2. Stelle Fragen zu deinen Unterlagen im Chat
            3. Erhalte Antworten mit präzisen Quellenangaben

            **Features:**
            - 📚 Mehrere PDF-Dokumente gleichzeitig verarbeiten
            - 💬 Konversationsbasierter Chat mit Kontext-Verständnis
            - 🔍 Automatische Quellenangaben mit Seitenzahlen
            - 🧠 Basiert auf GPT-4o-mini für präzise Antworten
            """
        )
    else:
        render_chat_interface()


if __name__ == "__main__":
    main()
