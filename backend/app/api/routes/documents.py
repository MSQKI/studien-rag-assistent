"""
Document Management API Routes
Endpoints for uploading and managing PDF documents.
"""

from typing import List
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel
from loguru import logger

from app.config import get_settings, Settings
from app.api.dependencies import get_rag_assistant, get_graph_builder
from app.services.document_pipeline import get_document_pipeline
from app.services.document_manager import get_document_manager

router = APIRouter()


# Response Models
class DocumentInfo(BaseModel):
    id: str
    filename: str
    file_size_bytes: int
    page_count: int | None = None
    chunk_count: int
    uploaded_at: datetime | None = None
    processed: bool
    subject: str | None = None


class DocumentListResponse(BaseModel):
    documents: List[DocumentInfo]
    total: int


class DocumentUploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    message: str
    details: dict | None = None


async def _process_document_background(
    file_path: Path,
    subject: str | None,
    document_id: str,
    filename: str
):
    """Background task for document processing."""
    try:
        logger.info(f"Starting background processing for {filename}")
        pipeline = get_document_pipeline()
        assistant = get_rag_assistant()
        graph_builder = get_graph_builder()

        result = await pipeline.process_document(
            file_path=file_path,
            subject=subject,
            assistant=assistant,
            graph_builder=graph_builder,
            document_id=document_id
        )

        logger.info(f"Background processing completed for {filename}: {result}")
    except Exception as e:
        logger.error(f"Background processing failed for {filename}: {str(e)}")


@router.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    subject: str | None = Query(None, description="Subject category"),
    settings: Settings = Depends(get_settings)
):
    """
    Upload a PDF document for processing.
    The document will be:
    1. Stored in the uploads directory
    2. Processed in the background (chunked, added to ChromaDB, entities extracted, flashcards generated)

    This endpoint returns IMMEDIATELY after file validation and saving.
    Processing happens asynchronously in the background.

    Args:
        background_tasks: FastAPI background tasks
        file: PDF file upload
        subject: Optional subject classification
        settings: Application settings

    Returns:
        Upload confirmation with document ID (processing continues in background)
    """
    try:
        # Validate file type
        if not file.filename.endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported"
            )

        # Check file size
        contents = await file.read()
        file_size_mb = len(contents) / (1024 * 1024)

        if file_size_mb > settings.max_upload_size_mb:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size: {settings.max_upload_size_mb}MB"
            )

        # Save file
        file_path = settings.upload_dir / file.filename
        with open(file_path, "wb") as f:
            f.write(contents)

        logger.info(f"Saved uploaded file: {file.filename} ({file_size_mb:.2f}MB)")

        # Generate document ID
        import uuid
        document_id = str(uuid.uuid4())

        # Add background task for processing
        background_tasks.add_task(
            _process_document_background,
            file_path=file_path,
            subject=subject,
            document_id=document_id,
            filename=file.filename
        )

        # Return immediately
        return DocumentUploadResponse(
            document_id=document_id,
            filename=file.filename,
            status="processing",
            message=f"Document uploaded successfully. Processing in background...",
            details={
                "file_size_mb": round(file_size_mb, 2),
                "subject": subject,
                "note": "Processing will complete in the background. Check stats to see progress."
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in document upload: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=DocumentListResponse)
async def list_documents(
    subject: str | None = Query(None, description="Filter by subject"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    settings: Settings = Depends(get_settings)
):
    """
    List all uploaded documents.

    Args:
        subject: Optional subject filter
        limit: Maximum number of documents to return
        offset: Number of documents to skip
        settings: Application settings

    Returns:
        List of documents with metadata
    """
    try:
        doc_manager = get_document_manager()
        documents = doc_manager.list_documents(subject=subject, limit=limit, offset=offset)

        return DocumentListResponse(
            documents=[DocumentInfo(**doc) for doc in documents],
            total=len(documents)
        )
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{document_id}", response_model=DocumentInfo)
async def get_document(
    document_id: str,
    settings: Settings = Depends(get_settings)
):
    """
    Get details for a specific document.

    Args:
        document_id: Document ID
        settings: Application settings

    Returns:
        Document details
    """
    try:
        doc_manager = get_document_manager()
        document = doc_manager.get_document(document_id)

        if not document:
            raise HTTPException(
                status_code=404,
                detail=f"Document '{document_id}' not found"
            )

        return DocumentInfo(**document)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error retrieving document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    delete_from_graph: bool = Query(True, description="Delete from Neo4j"),
    delete_flashcards: bool = Query(True, description="Delete associated flashcards"),
    settings: Settings = Depends(get_settings)
):
    """
    Delete a document and all associated data.
    This will remove:
    - The physical PDF file
    - Vector embeddings from ChromaDB
    - Graph entities from Neo4j (if delete_from_graph=true)
    - Associated flashcards (if delete_flashcards=true)

    Args:
        document_id: Document ID
        delete_from_graph: Whether to delete from Neo4j
        delete_flashcards: Whether to delete flashcards
        settings: Application settings

    Returns:
        Deletion confirmation with details
    """
    try:
        doc_manager = get_document_manager()

        # Check if document exists
        document = doc_manager.get_document(document_id)
        if not document:
            raise HTTPException(
                status_code=404,
                detail=f"Document '{document_id}' not found"
            )

        # Delete document
        results = doc_manager.delete_document(
            document_id=document_id,
            delete_from_graph=delete_from_graph,
            delete_flashcards=delete_flashcards
        )

        return {
            "message": f"Document '{document_id}' deleted successfully",
            "details": results
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{document_id}/generate-flashcards")
async def generate_more_flashcards(
    document_id: str,
    count: int = Query(20, ge=1, le=50, description="Number of flashcards to generate"),
    settings: Settings = Depends(get_settings)
):
    """
    Generate additional flashcards for an existing document.

    Args:
        document_id: Document ID
        count: Number of flashcards to generate (1-50)
        settings: Application settings

    Returns:
        Generation results
    """
    try:
        from app.services.flashcards.flashcard_generator import FlashcardGenerator
        from app.services.rag.document_processor import DocumentProcessor
        from app.services.document_manager import get_document_manager

        doc_manager = get_document_manager()

        # Check if document exists
        document = doc_manager.get_document(document_id)
        if not document:
            raise HTTPException(
                status_code=404,
                detail=f"Document '{document_id}' not found"
            )

        # Get document path
        file_path = settings.upload_dir / document["filename"]
        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Document file not found: {document['filename']}"
            )

        logger.info(f"Generating {count} additional flashcards for {document['filename']}")

        # Process document to get chunks
        doc_processor = DocumentProcessor()
        documents = doc_processor.process_pdf(file_path)

        # Generate flashcards
        flashcard_generator = FlashcardGenerator()
        flashcards = await flashcard_generator.generate_from_documents(
            documents=documents,
            subject=document.get("subject") or "General",
            document_id=document_id,
            count=count
        )

        return {
            "message": f"Successfully generated {len(flashcards)} additional flashcards",
            "document_id": document_id,
            "filename": document["filename"],
            "flashcards_generated": len(flashcards),
            "flashcard_ids": [fc["id"] for fc in flashcards]
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating flashcards: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{document_id}/reprocess")
async def reprocess_document(
    document_id: str,
    settings: Settings = Depends(get_settings)
):
    """
    Reprocess a document (useful after configuration changes).

    Args:
        document_id: Document ID
        settings: Application settings

    Returns:
        Reprocessing confirmation
    """
    # TODO: Implement document reprocessing
    raise HTTPException(
        status_code=501,
        detail="Document reprocessing not yet implemented"
    )


@router.get("/{document_id}/download")
async def download_document(
    document_id: str,
    settings: Settings = Depends(get_settings)
):
    """
    Download the original PDF file.

    Args:
        document_id: Document ID
        settings: Application settings

    Returns:
        PDF file
    """
    # TODO: Implement document download
    raise HTTPException(
        status_code=404,
        detail=f"Document '{document_id}' not found"
    )
