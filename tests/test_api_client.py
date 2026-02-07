import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from mcp_lightrag.api_client import LightRAGApiClient, with_retry
from mcp_lightrag.models import ServerSettings
from mcp_lightrag.exceptions import APIResponseError
from mcp_lightrag.client.light_rag_server_api_client.errors import UnexpectedStatus

@pytest.fixture
def settings():
    return ServerSettings(host="localhost", port=9621, api_key="test")

@pytest.mark.asyncio
async def test_retry_logic():
    mock_func = AsyncMock()
    # Mock failure twice, then success
    mock_func.side_effect = [
        UnexpectedStatus(status_code=500, content=b"error"),
        UnexpectedStatus(status_code=500, content=b"error"),
        "success"
    ]
    
    @with_retry(max_retries=3, base_delay=0.01)
    async def decorated():
        return await mock_func()
        
    result = await decorated()
    assert result == "success"
    assert mock_func.call_count == 3

@pytest.mark.asyncio
async def test_retry_logic_failure():
    mock_func = AsyncMock()
    mock_func.side_effect = UnexpectedStatus(status_code=500, content=b"error")
    
    @with_retry(max_retries=2, base_delay=0.01)
    async def decorated():
        return await mock_func()
        
    with pytest.raises(UnexpectedStatus):
        await decorated()
    assert mock_func.call_count == 2

@pytest.mark.asyncio
async def test_client_init(settings):
    with patch("mcp_lightrag.api_client.AuthenticatedClient") as mock_auth:
        client = LightRAGApiClient(settings)
        assert client.settings == settings
        mock_auth.assert_called_once_with(
            base_url="http://localhost:9621",
            token="test",
            verify_ssl=False
        )


# --- Document Operation Tests ---

@pytest.fixture
def mock_client(settings):
    """Create a LightRAGApiClient with mocked AuthenticatedClient."""
    with patch("mcp_lightrag.api_client.AuthenticatedClient"):
        client = LightRAGApiClient(settings)
        yield client


@pytest.mark.asyncio
async def test_ingest_file(mock_client, tmp_path):
    """Test uploading a file (ingest_file operation)."""
    # Create a sample file to upload
    sample_file = tmp_path / "sample.txt"
    sample_file.write_text("Sample content for testing")
    
    with patch("mcp_lightrag.api_client.async_upload_document", new_callable=AsyncMock) as mock_upload:
        mock_upload.return_value = {"status": "success", "filename": "sample.txt"}
        
        result = await mock_client.upload_file(sample_file)
        
        assert result["status"] == "success"
        mock_upload.assert_called_once()


@pytest.mark.asyncio
async def test_ingest_file_readme(mock_client):
    """Test uploading README.md file."""
    from pathlib import Path
    readme_path = Path(__file__).parent.parent / "README.md"
    
    with patch("mcp_lightrag.api_client.async_upload_document", new_callable=AsyncMock) as mock_upload:
        mock_upload.return_value = {"status": "success", "filename": "README.md"}
        
        result = await mock_client.upload_file(readme_path)
        
        assert result["status"] == "success"
        mock_upload.assert_called_once()


@pytest.mark.asyncio
async def test_ingest_file_pyproject(mock_client):
    """Test uploading pyproject.toml file."""
    from pathlib import Path
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    
    with patch("mcp_lightrag.api_client.async_upload_document", new_callable=AsyncMock) as mock_upload:
        mock_upload.return_value = {"status": "success", "filename": "pyproject.toml"}
        
        result = await mock_client.upload_file(pyproject_path)
        
        assert result["status"] == "success"
        mock_upload.assert_called_once()


@pytest.mark.asyncio
async def test_ingest_file_not_found(mock_client):
    """Test that uploading a non-existent file raises ResourceNotFoundError."""
    from mcp_lightrag.exceptions import ResourceNotFoundError
    
    with pytest.raises(ResourceNotFoundError):
        await mock_client.upload_file("/non/existent/file.txt")


@pytest.mark.asyncio
async def test_ingest_text(mock_client):
    """Test inserting text content (ingest_text operation)."""
    # First phrases from README.md
    sample_text = "A Model Context Protocol (MCP) server that enables AI assistants to interact with LightRAG knowledge graphs. Query documents, manage entities, and build semantic relationships through a standardized tool interface."
    
    with patch("mcp_lightrag.api_client.async_insert_document", new_callable=AsyncMock) as mock_insert:
        mock_insert.return_value = {"status": "success", "message": "Text inserted successfully"}
        
        result = await mock_client.add_text(sample_text)
        
        assert result["status"] == "success"
        mock_insert.assert_called_once()


@pytest.mark.asyncio
async def test_ingest_text_multiple(mock_client):
    """Test inserting multiple text contents at once."""
    texts = [
        "A Model Context Protocol (MCP) server that enables AI assistants to interact with LightRAG knowledge graphs.",
        "Query documents, manage entities, and build semantic relationships through a standardized tool interface."
    ]
    
    with patch("mcp_lightrag.api_client.async_insert_texts", new_callable=AsyncMock) as mock_insert:
        mock_insert.return_value = {"status": "success", "count": 2}
        
        result = await mock_client.add_text(texts)
        
        assert result["status"] == "success"
        mock_insert.assert_called_once()


@pytest.mark.asyncio
async def test_ingest_batch(mock_client, tmp_path):
    """Test batch ingestion from a directory (ingest_batch operation)."""
    # Create sample files in a temporary directory
    (tmp_path / "file1.txt").write_text("Content 1")
    (tmp_path / "file2.txt").write_text("Content 2")
    (tmp_path / "file3.md").write_text("# Markdown content")
    
    with patch("mcp_lightrag.api_client.async_upload_document", new_callable=AsyncMock) as mock_upload:
        mock_upload.return_value = {"status": "success"}
        
        result = await mock_client.ingest_batch(tmp_path)
        
        assert result["total"] == 3
        assert result["successful"] == 3
        assert result["failed"] == 0
        assert len(result["details"]) == 3


@pytest.mark.asyncio
async def test_ingest_batch_with_filter(mock_client, tmp_path):
    """Test batch ingestion with file type filter."""
    # Create sample files
    (tmp_path / "file1.txt").write_text("Content 1")
    (tmp_path / "file2.md").write_text("# Markdown content")
    
    with patch("mcp_lightrag.api_client.async_upload_document", new_callable=AsyncMock) as mock_upload:
        mock_upload.return_value = {"status": "success"}
        
        # Filter to only include .md files
        result = await mock_client.ingest_batch(tmp_path, include_only=[r"\.md$"])
        
        assert result["total"] == 1
        assert result["successful"] == 1


@pytest.mark.asyncio
async def test_ingest_batch_directory_not_found(mock_client):
    """Test that batch ingestion with non-existent directory raises ResourceNotFoundError."""
    from mcp_lightrag.exceptions import ResourceNotFoundError
    
    with pytest.raises(ResourceNotFoundError):
        await mock_client.ingest_batch("/non/existent/directory")


@pytest.mark.asyncio
async def test_upload_and_index(mock_client, tmp_path):
    """Test upload and index operation (upload_file + scan_inputs)."""
    sample_file = tmp_path / "document.txt"
    sample_file.write_text("Document content for indexing")
    
    with patch("mcp_lightrag.api_client.async_upload_document", new_callable=AsyncMock) as mock_upload, \
         patch("mcp_lightrag.api_client.async_scan_for_new_documents", new_callable=AsyncMock) as mock_scan:
        mock_upload.return_value = {"status": "uploaded", "filename": "document.txt"}
        mock_scan.return_value = {"status": "scanning", "files_found": 1}
        
        # Upload file
        upload_result = await mock_client.upload_file(sample_file)
        assert upload_result["status"] == "uploaded"
        
        # Trigger scan/index
        scan_result = await mock_client.scan_inputs()
        assert scan_result["status"] == "scanning"


@pytest.mark.asyncio
async def test_list_all_docs(mock_client):
    """Test listing all indexed documents (list_all_docs operation)."""
    with patch("mcp_lightrag.api_client.async_get_documents", new_callable=AsyncMock) as mock_get_docs:
        mock_get_docs.return_value = {
            "documents": [
                {"id": "doc1", "name": "README.md", "status": "indexed"},
                {"id": "doc2", "name": "pyproject.toml", "status": "indexed"}
            ],
            "total": 2
        }
        
        result = await mock_client.get_all_documents()
        
        assert result["total"] == 2
        assert len(result["documents"]) == 2
        mock_get_docs.assert_called_once()


@pytest.mark.asyncio
async def test_check_indexing_status(mock_client):
    """Test checking indexing pipeline status (check_indexing_status operation)."""
    with patch("mcp_lightrag.api_client.async_get_pipeline_status", new_callable=AsyncMock) as mock_status:
        mock_status.return_value = {
            "status": "idle",
            "pending_files": 0,
            "processing_files": 0,
            "completed_files": 5,
            "failed_files": 0
        }
        
        result = await mock_client.get_pipeline_status()
        
        assert result["status"] == "idle"
        assert result["pending_files"] == 0
        mock_status.assert_called_once()


@pytest.mark.asyncio
async def test_check_indexing_status_busy(mock_client):
    """Test indexing status when pipeline is processing."""
    with patch("mcp_lightrag.api_client.async_get_pipeline_status", new_callable=AsyncMock) as mock_status:
        mock_status.return_value = {
            "status": "processing",
            "pending_files": 2,
            "processing_files": 1,
            "completed_files": 10,
            "failed_files": 0
        }
        
        result = await mock_client.get_pipeline_status()
        
        assert result["status"] == "processing"
        assert result["pending_files"] == 2


@pytest.mark.asyncio
async def test_verify_server_health(mock_client):
    """Test server health check (verify_server_health operation)."""
    with patch("mcp_lightrag.api_client.async_get_health", new_callable=AsyncMock) as mock_health:
        mock_health.return_value = {
            "status": "healthy",
            "version": "1.0.0",
            "uptime": 3600
        }
        
        result = await mock_client.check_health()
        
        assert result["status"] == "healthy"
        mock_health.assert_called_once()


@pytest.mark.asyncio
async def test_verify_server_health_unhealthy(mock_client):
    """Test server health check when server is unhealthy."""
    with patch("mcp_lightrag.api_client.async_get_health", new_callable=AsyncMock) as mock_health:
        mock_health.return_value = {
            "status": "degraded",
            "version": "1.0.0",
            "issues": ["High memory usage"]
        }
        
        result = await mock_client.check_health()
        
        assert result["status"] == "degraded"
        assert "issues" in result
