"""
Example test file for configuration module.
"""

import pytest
from pathlib import Path
from backend.app.config import Settings, get_settings, reload_settings


class TestSettings:
    """Test cases for Settings configuration."""

    def test_settings_default_values(self, monkeypatch):
        """Test that default values are set correctly."""
        # Mock the OpenAI API key
        monkeypatch.setenv("OPENAI_API_KEY", "test_key_12345")

        settings = Settings()

        assert settings.openai_api_key == "test_key_12345"
        assert settings.embedding_model == "text-embedding-3-small"
        assert settings.llm_model == "gpt-4o-mini"
        assert settings.temperature == 0.2
        assert settings.max_tokens == 2000
        assert settings.chunk_size == 1000
        assert settings.chunk_overlap == 200

    def test_chunk_overlap_validation(self, monkeypatch):
        """Test that chunk overlap validation works."""
        monkeypatch.setenv("OPENAI_API_KEY", "test_key_12345")
        monkeypatch.setenv("CHUNK_SIZE", "1000")
        monkeypatch.setenv("CHUNK_OVERLAP", "1000")

        with pytest.raises(ValueError, match="chunk_overlap must be less than chunk_size"):
            Settings()

    def test_temperature_bounds(self, monkeypatch):
        """Test that temperature is bounded correctly."""
        monkeypatch.setenv("OPENAI_API_KEY", "test_key_12345")
        monkeypatch.setenv("TEMPERATURE", "3.0")

        with pytest.raises(ValueError):
            Settings()

    def test_get_settings_singleton(self, monkeypatch):
        """Test that get_settings returns the same instance."""
        monkeypatch.setenv("OPENAI_API_KEY", "test_key_12345")

        # Reset global settings
        reload_settings()

        settings1 = get_settings()
        settings2 = get_settings()

        assert settings1 is settings2

    def test_create_directories(self, tmp_path, monkeypatch):
        """Test that directories are created correctly."""
        monkeypatch.setenv("OPENAI_API_KEY", "test_key_12345")
        monkeypatch.setenv("CHROMA_PERSIST_DIR", str(tmp_path / "chroma"))
        monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))

        settings = Settings()
        settings.create_directories()

        assert settings.chroma_persist_dir.exists()
        assert settings.upload_dir.exists()


class TestSettingsFromEnv:
    """Test cases for loading settings from environment."""

    def test_load_custom_model(self, monkeypatch):
        """Test loading custom model from environment."""
        monkeypatch.setenv("OPENAI_API_KEY", "test_key_12345")
        monkeypatch.setenv("LLM_MODEL", "gpt-4")
        monkeypatch.setenv("EMBEDDING_MODEL", "text-embedding-ada-002")

        settings = Settings()

        assert settings.llm_model == "gpt-4"
        assert settings.embedding_model == "text-embedding-ada-002"

    def test_load_custom_paths(self, monkeypatch):
        """Test loading custom paths from environment."""
        monkeypatch.setenv("OPENAI_API_KEY", "test_key_12345")
        monkeypatch.setenv("CHROMA_PERSIST_DIR", "/custom/chroma")
        monkeypatch.setenv("UPLOAD_DIR", "/custom/uploads")

        settings = Settings()

        assert settings.chroma_persist_dir == Path("/custom/chroma")
        assert settings.upload_dir == Path("/custom/uploads")


# Fixture for test environment setup
@pytest.fixture(autouse=True)
def reset_settings():
    """Reset global settings before each test."""
    reload_settings()
    yield
    reload_settings()
