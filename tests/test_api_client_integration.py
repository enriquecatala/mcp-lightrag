"""
Integration tests for LightRAG API client.

These tests require a running LightRAG server. Configure connection via .env file:
    LIGHTRAG_API_HOST="localhost"
    LIGHTRAG_API_PORT=9621
    LIGHTRAG_API_KEY="your-api-key"

Tests will be skipped if the server is not available.
"""

import os
import pytest
from pathlib import Path
from dotenv import load_dotenv

from mcp_lightrag.api_client import LightRAGApiClient
from mcp_lightrag.models import ServerSettings

# Load environment variables from .env file
load_dotenv()


def get_settings() -> ServerSettings:
    """Create settings from environment variables."""
    return ServerSettings(
        host=os.getenv("LIGHTRAG_API_HOST", "localhost"),
        port=int(os.getenv("LIGHTRAG_API_PORT", "9621")),
        api_key=os.getenv("LIGHTRAG_API_KEY", "")
    )


async def is_server_available() -> bool:
    """Check if the LightRAG server is reachable."""
    try:
        settings = get_settings()
        client = LightRAGApiClient(settings)
        await client.check_health()
        await client.close()
        return True
    except Exception:
        return False


@pytest.fixture
async def client():
    """Create an API client for integration tests."""
    settings = get_settings()
    api_client = LightRAGApiClient(settings)
    yield api_client
    await api_client.close()


# Mark all tests to be skipped if server is not available
pytestmark = pytest.mark.asyncio


# --- Sample data paths ---
PROJECT_ROOT = Path(__file__).parent.parent
README_PATH = PROJECT_ROOT / "README.md"
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"

# First phrases from README.md for text ingestion
SAMPLE_TEXT = (
    "A Model Context Protocol (MCP) server that enables AI assistants to interact with "
    "LightRAG knowledge graphs. Query documents, manage entities, and build semantic "
    "relationships through a standardized tool interface."
)


# --- Integration Tests ---

@pytest.mark.integration
async def test_verify_server_health(client):
    """Test server health check against running LightRAG server."""
    result = await client.check_health()
    
    # Server should respond with health status
    assert result is not None
    print(f"Server health: {result}")


@pytest.mark.integration
async def test_ingest_text(client):
    """Test inserting text content into running LightRAG server."""
    result = await client.add_text(SAMPLE_TEXT)
    
    assert result is not None
    print(f"Text ingestion result: {result}")


@pytest.mark.integration
async def test_ingest_text_multiple(client):
    """Test inserting multiple text contents at once."""
    texts = [
        "A Model Context Protocol (MCP) server that enables AI assistants to interact with LightRAG knowledge graphs.",
        "Query documents, manage entities, and build semantic relationships through a standardized tool interface."
    ]
    
    result = await client.add_text(texts)
    
    assert result is not None
    print(f"Multiple text ingestion result: {result}")


@pytest.mark.integration
async def test_ingest_file_readme(client):
    """Test uploading README.md file to running LightRAG server."""
    if not README_PATH.exists():
        pytest.skip(f"README.md not found at {README_PATH}")
    
    result = await client.upload_file(README_PATH)
    
    assert result is not None
    print(f"README.md upload result: {result}")


@pytest.mark.integration
async def test_ingest_file_pyproject(client):
    """Test uploading pyproject.toml file to running LightRAG server."""
    if not PYPROJECT_PATH.exists():
        pytest.skip(f"pyproject.toml not found at {PYPROJECT_PATH}")
    
    result = await client.upload_file(PYPROJECT_PATH)
    
    assert result is not None
    print(f"pyproject.toml upload result: {result}")


@pytest.mark.integration
async def test_ingest_batch(client, tmp_path):
    """Test batch ingestion from a directory."""
    # Create sample files in a temporary directory
    (tmp_path / "test_file1.txt").write_text("Content for batch test file 1")
    (tmp_path / "test_file2.txt").write_text("Content for batch test file 2")
    (tmp_path / "test_file3.md").write_text("# Markdown batch test content")
    
    result = await client.ingest_batch(tmp_path)
    
    assert result is not None
    assert result["total"] == 3
    print(f"Batch ingestion result: {result}")


@pytest.mark.integration
async def test_upload_and_index(client, tmp_path):
    """Test upload and trigger indexing scan."""
    sample_file = tmp_path / "upload_test_document.txt"
    sample_file.write_text("Document content for upload and index integration test")
    
    # Upload file
    upload_result = await client.upload_file(sample_file)
    assert upload_result is not None
    print(f"Upload result: {upload_result}")
    
    # Trigger scan for new documents
    scan_result = await client.scan_inputs()
    assert scan_result is not None
    print(f"Scan result: {scan_result}")


@pytest.mark.integration
async def test_list_all_docs(client):
    """Test listing all indexed documents from running LightRAG server."""
    result = await client.get_all_documents()
    
    assert result is not None
    print(f"Documents list: {result}")


@pytest.mark.integration
async def test_check_indexing_status(client):
    """Test checking indexing pipeline status on running LightRAG server."""
    result = await client.get_pipeline_status()
    
    assert result is not None
    print(f"Pipeline status: {result}")


# --- Skip integration tests if server is not available ---

@pytest.fixture(scope="module", autouse=True)
def skip_if_no_server():
    """Skip all integration tests if server is not available."""
    import asyncio
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        available = loop.run_until_complete(is_server_available())
        loop.close()
    except Exception:
        available = False
    
    if not available:
        pytest.skip("LightRAG server is not available. Skipping integration tests.")

