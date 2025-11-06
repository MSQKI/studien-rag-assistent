#!/usr/bin/env python3
"""
Entry point for running the Studien-RAG-Assistent locally.
"""

import sys
import subprocess
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def check_environment():
    """Check if the environment is properly configured."""
    from src.config import get_settings

    try:
        settings = get_settings()
        print("✅ Environment configuration loaded successfully")
        print(f"   - LLM Model: {settings.llm_model}")
        print(f"   - Embedding Model: {settings.embedding_model}")
        print(f"   - ChromaDB Path: {settings.chroma_persist_dir}")
        return True
    except Exception as e:
        print(f"❌ Environment configuration error: {str(e)}")
        print("\nMake sure you have:")
        print("1. Created a .env file (copy from .env.example)")
        print("2. Set your OPENAI_API_KEY in the .env file")
        return False


def main():
    """Main entry point."""
    print("=" * 60)
    print("🎓 Studien-RAG-Assistent")
    print("=" * 60)
    print()

    # Check environment
    if not check_environment():
        sys.exit(1)

    print()
    print("Starting Streamlit application...")
    print("=" * 60)
    print()

    # Run Streamlit
    try:
        subprocess.run(
            [
                "streamlit",
                "run",
                "src/ui.py",
                "--server.port=8501",
                "--server.address=localhost",
            ],
            check=True,
        )
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error running Streamlit: {str(e)}")
        sys.exit(1)
    except FileNotFoundError:
        print("\n❌ Streamlit not found. Please install requirements:")
        print("   pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()
