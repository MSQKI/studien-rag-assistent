"""
Advanced Document Processor with Multimodal Support
Handles tables, images, and complex layouts using state-of-the-art 2025 techniques.
"""

import base64
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from io import BytesIO

from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

from app.config import get_settings

logger = logging.getLogger(__name__)


class AdvancedDocumentProcessor:
    """
    Advanced PDF processor using Unstructured.io for tables, images, and complex layouts.
    Falls back to standard processing if advanced features unavailable.
    """

    def __init__(self):
        """Initialize the advanced document processor."""
        self.settings = get_settings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.settings.chunk_size,
            chunk_overlap=self.settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""],
            is_separator_regex=False,
        )

        # Check if advanced libraries are available
        self.has_unstructured = self._check_unstructured()
        self.has_vision = self._check_vision()

        if self.has_unstructured:
            logger.info("✅ Unstructured.io available - Enhanced table/image extraction enabled")
        else:
            logger.warning("⚠️  Unstructured.io not available - Using fallback processing")

    def _check_unstructured(self) -> bool:
        """Check if unstructured library is available."""
        try:
            import unstructured  # noqa: F401
            return True
        except ImportError:
            return False

    def _check_vision(self) -> bool:
        """Check if GPT-4 Vision is available."""
        try:
            # Check if we have OpenAI key
            return bool(self.settings.openai_api_key)
        except Exception:
            return False

    def process_pdf_with_unstructured(self, file_path: Path) -> List[Document]:
        """
        Process PDF using Unstructured.io for enhanced table/image extraction.

        Args:
            file_path: Path to PDF file

        Returns:
            List of Document objects with tables and images as text
        """
        try:
            from unstructured.partition.pdf import partition_pdf
            from unstructured.chunking.title import chunk_by_title

            logger.info(f"Processing {file_path.name} with Unstructured.io")

            # Partition PDF into elements (text, tables, images)
            elements = partition_pdf(
                filename=str(file_path),
                strategy="hi_res",  # High resolution for tables/images
                infer_table_structure=True,  # Extract table structure
                extract_images_in_pdf=True,  # Extract images
                extract_image_block_types=["Image", "Table"],  # What to extract
                extract_image_block_to_payload=False,  # Don't embed images in payload
            )

            logger.info(f"Extracted {len(elements)} elements from {file_path.name}")

            # Chunk elements while preserving structure
            chunks = chunk_by_title(
                elements,
                max_characters=self.settings.chunk_size,
                combine_text_under_n_chars=self.settings.chunk_overlap,
                new_after_n_chars=self.settings.chunk_size,
            )

            # Convert to LangChain Documents
            documents = []
            for i, chunk in enumerate(chunks):
                # Get element type
                element_type = chunk.metadata.get("type", "NarrativeText")

                # Prepare content
                content = str(chunk)

                # Add special handling for tables
                if element_type == "Table":
                    # Try to format as markdown table
                    content = f"[TABLE]\n{content}\n[/TABLE]"
                    logger.debug(f"Found table in chunk {i}")

                # Create metadata
                metadata = {
                    "source_file": file_path.name,
                    "file_path": str(file_path),
                    "chunk_id": i,
                    "chunk_size": len(content),
                    "element_type": element_type,
                    "page_number": chunk.metadata.get("page_number", None),
                }

                # Add coordinates if available (for image retrieval)
                if "coordinates" in chunk.metadata:
                    metadata["coordinates"] = chunk.metadata["coordinates"]

                doc = Document(
                    page_content=content,
                    metadata=metadata
                )
                documents.append(doc)

            logger.info(f"Created {len(documents)} chunks from {file_path.name}")
            return documents

        except Exception as e:
            logger.error(f"Unstructured processing failed for {file_path.name}: {str(e)}")
            logger.info("Falling back to standard processing")
            return self._fallback_processing(file_path)

    def _fallback_processing(self, file_path: Path) -> List[Document]:
        """
        Fallback to standard PyPDF processing.

        Args:
            file_path: Path to PDF file

        Returns:
            List of Document objects
        """
        try:
            from langchain_community.document_loaders import PyPDFLoader

            logger.info(f"Using fallback PyPDF processing for {file_path.name}")
            loader = PyPDFLoader(str(file_path))
            documents = loader.load()

            # Enrich metadata
            for doc in documents:
                doc.metadata["source_file"] = file_path.name
                doc.metadata["file_path"] = str(file_path)
                doc.metadata["element_type"] = "Text"

            # Split into chunks
            chunks = self.text_splitter.split_documents(documents)

            # Add chunk metadata
            for i, chunk in enumerate(chunks):
                chunk.metadata["chunk_id"] = i
                chunk.metadata["chunk_size"] = len(chunk.page_content)

            logger.info(f"Created {len(chunks)} chunks from {file_path.name}")
            return chunks

        except Exception as e:
            logger.error(f"Fallback processing failed: {str(e)}")
            raise

    async def process_images_with_vision(
        self,
        file_path: Path,
        documents: List[Document]
    ) -> List[Document]:
        """
        Enhance documents with GPT-4 Vision descriptions of images/tables.

        Args:
            file_path: Path to PDF file
            documents: Documents from unstructured processing

        Returns:
            Enhanced documents with image descriptions
        """
        if not self.has_vision:
            logger.info("GPT-4 Vision not available, skipping image enhancement")
            return documents

        try:
            from openai import AsyncOpenAI
            import pdf2image

            logger.info("Enhancing documents with GPT-4 Vision")
            client = AsyncOpenAI(api_key=self.settings.openai_api_key)

            # Convert PDF to images
            images = pdf2image.convert_from_path(str(file_path))

            # Track which documents have been enhanced
            enhanced_docs = []

            for doc in documents:
                # Check if document contains table or is from a page with images
                element_type = doc.metadata.get("element_type", "")
                page_num = doc.metadata.get("page_number", None)

                if element_type in ["Table", "Image"] and page_num is not None:
                    # Get corresponding page image
                    if 0 <= page_num - 1 < len(images):
                        page_image = images[page_num - 1]

                        # Convert to base64
                        buffered = BytesIO()
                        page_image.save(buffered, format="PNG")
                        img_base64 = base64.b64encode(buffered.getvalue()).decode()

                        # Ask GPT-4 Vision to describe
                        response = await client.chat.completions.create(
                            model="gpt-4o",  # Use gpt-4o for vision
                            messages=[
                                {
                                    "role": "user",
                                    "content": [
                                        {
                                            "type": "text",
                                            "text": "Describe this table or image in detail. "
                                                    "If it's a table, extract all data in a structured format. "
                                                    "If it's an image, describe what you see and any relevant information."
                                        },
                                        {
                                            "type": "image_url",
                                            "image_url": {
                                                "url": f"data:image/png;base64,{img_base64}"
                                            }
                                        }
                                    ]
                                }
                            ],
                            max_tokens=1000
                        )

                        # Add vision description to document
                        vision_desc = response.choices[0].message.content
                        doc.page_content += f"\n\n[VISION DESCRIPTION]\n{vision_desc}\n[/VISION DESCRIPTION]"
                        doc.metadata["enhanced_with_vision"] = True

                        logger.debug(f"Enhanced chunk {doc.metadata['chunk_id']} with vision")

                enhanced_docs.append(doc)

            logger.info(f"Enhanced {sum(1 for d in enhanced_docs if d.metadata.get('enhanced_with_vision'))} documents with vision")
            return enhanced_docs

        except Exception as e:
            logger.error(f"Vision enhancement failed: {str(e)}")
            return documents

    async def process_pdf(
        self,
        file_path: Path,
        use_vision: bool = False
    ) -> List[Document]:
        """
        Main processing pipeline - uses best available method.

        Args:
            file_path: Path to PDF file
            use_vision: Whether to use GPT-4 Vision for images (slower, costs more)

        Returns:
            List of processed documents
        """
        try:
            # Use unstructured if available
            if self.has_unstructured:
                documents = self.process_pdf_with_unstructured(file_path)
            else:
                documents = self._fallback_processing(file_path)

            # Optionally enhance with vision
            if use_vision and self.has_vision:
                documents = await self.process_images_with_vision(file_path, documents)

            logger.info(
                f"Processed {file_path.name}: {len(documents)} chunks "
                f"(unstructured={self.has_unstructured}, vision={use_vision and self.has_vision})"
            )
            return documents

        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            raise


# Convenience function for backward compatibility
def get_advanced_processor() -> AdvancedDocumentProcessor:
    """Get global advanced processor instance."""
    return AdvancedDocumentProcessor()
