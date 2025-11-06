# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2024-11-05

### Added
- Initial release of Studien-RAG-Assistent
- PDF document processing with PyPDFLoader
- Intelligent text chunking with RecursiveCharacterTextSplitter
- ChromaDB integration for persistent vector storage
- OpenAI embeddings (text-embedding-3-small)
- Chat interface with GPT-4o-mini
- Automatic source citations with page numbers
- Conversation memory for context-aware responses
- Streamlit web interface
- Docker support with docker-compose
- Batch processing for multiple PDFs
- Document management (upload, delete)
- Comprehensive test suite
- Development tools (black, isort, flake8, mypy)
- Pre-commit hooks for code quality
- Extensive documentation (README, CONTRIBUTING)

### Features
- **Core RAG Pipeline**: LangChain-based RAG implementation
- **Vector Store**: Local ChromaDB with persistent storage
- **Chat Interface**: Modern Streamlit UI with source display
- **Document Processing**: Automatic PDF chunking with metadata
- **Citations**: Automatic source references with page numbers
- **Memory**: Conversation history for context-aware answers
- **Docker**: Production-ready containerization
- **Testing**: Pytest with coverage reporting
- **Code Quality**: Automated formatting and linting

### Configuration
- Flexible configuration via .env file
- Customizable chunk size and overlap
- Adjustable LLM parameters (temperature, max tokens)
- Configurable retrieval settings

### Documentation
- Comprehensive README with installation guide
- Contributing guidelines
- Architecture documentation
- API documentation in docstrings
- Example configurations

## Types of Changes
- `Added` for new features
- `Changed` for changes in existing functionality
- `Deprecated` for soon-to-be removed features
- `Removed` for now removed features
- `Fixed` for any bug fixes
- `Security` in case of vulnerabilities
