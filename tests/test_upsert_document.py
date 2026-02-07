"""
Unit tests for upsert_document functionality.

Tests cover all scenarios:
- Document doesn't exist → creates it
- Document exists and is identical → skips
- Document exists but was modified (word removed) → updates
- Document exists but was modified (word added) → updates
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from pathlib import Path

from mcp_lightrag.api_client import LightRAGApiClient
from mcp_lightrag.models import ServerSettings


@pytest.fixture
def settings():
    return ServerSettings(host="localhost", port=9621, api_key="test")


@pytest.fixture
def mock_client(settings):
    """Create a LightRAGApiClient with mocked AuthenticatedClient."""
    with patch("mcp_lightrag.api_client.AuthenticatedClient"):
        client = LightRAGApiClient(settings)
        yield client


@pytest.fixture
def test_doc_path():
    """Path to the test document."""
    return Path(__file__).parent / "test_upsert_doc.txt"


class MockExistingDoc:
    """Mock object simulating an existing document from the API."""
    def __init__(self, doc_id: str, content_length: int, file_path: str):
        self.id = doc_id
        self.content_length = content_length
        self.file_path = file_path


@pytest.mark.asyncio
async def test_upsert_document_new(mock_client, test_doc_path):
    """Test upsert when document doesn't exist - should create it."""
    with patch.object(mock_client, "find_document_by_file_name", new_callable=AsyncMock) as mock_find, \
         patch.object(mock_client, "upload_file", new_callable=AsyncMock) as mock_upload:
        
        # Document doesn't exist
        mock_find.return_value = None
        mock_upload.return_value = {"status": "success", "filename": "test_upsert_doc.txt"}
        
        result = await mock_client.upsert_document(test_doc_path)
        
        assert result["action"] == "created"
        assert result["file_name"] == "test_upsert_doc.txt"
        mock_find.assert_called_once_with("test_upsert_doc.txt")
        mock_upload.assert_called_once_with(test_doc_path)


@pytest.mark.asyncio
async def test_upsert_document_identical(mock_client, test_doc_path):
    """Test upsert when document exists and is identical - should skip."""
    # Get actual file size
    actual_size = len(test_doc_path.read_bytes())
    
    with patch.object(mock_client, "find_document_by_file_name", new_callable=AsyncMock) as mock_find, \
         patch.object(mock_client, "upload_file", new_callable=AsyncMock) as mock_upload, \
         patch.object(mock_client, "delete_by_doc", new_callable=AsyncMock) as mock_delete:
        
        # Document exists with same content length
        mock_find.return_value = MockExistingDoc(
            doc_id="doc-123",
            content_length=actual_size,
            file_path="/inputs/test_upsert_doc.txt"
        )
        
        result = await mock_client.upsert_document(test_doc_path)
        
        assert result["action"] == "skipped"
        assert result["reason"] == "document already exists with identical content"
        assert result["doc_id"] == "doc-123"
        mock_find.assert_called_once()
        mock_upload.assert_not_called()
        mock_delete.assert_not_called()


@pytest.mark.asyncio
async def test_upsert_document_modified_removed_word(mock_client, tmp_path):
    """Test upsert when document was modified (word removed) - should update."""
    # Create a modified version of the test doc with a word removed
    modified_doc = tmp_path / "test_upsert_doc.txt"
    modified_doc.write_text("This is a test document for upsert testing.\nIt contains a few lines to verify upsert.\nLine three.\n")
    
    # Original size (from the actual test file)
    original_size = len(Path(__file__).parent.joinpath("test_upsert_doc.txt").read_bytes())
    
    with patch.object(mock_client, "find_document_by_file_name", new_callable=AsyncMock) as mock_find, \
         patch.object(mock_client, "upload_file", new_callable=AsyncMock) as mock_upload, \
         patch.object(mock_client, "delete_by_doc", new_callable=AsyncMock) as mock_delete:
        
        # Document exists but with different content length (original was longer)
        mock_find.return_value = MockExistingDoc(
            doc_id="doc-456",
            content_length=original_size,  # Different from modified file
            file_path="/inputs/test_upsert_doc.txt"
        )
        mock_delete.return_value = {"status": "deleted"}
        mock_upload.return_value = {"status": "success"}
        
        result = await mock_client.upsert_document(modified_doc)
        
        assert result["action"] == "updated"
        assert result["old_doc_id"] == "doc-456"
        mock_find.assert_called_once()
        mock_delete.assert_called_once_with("doc-456")
        mock_upload.assert_called_once_with(modified_doc)


@pytest.mark.asyncio
async def test_upsert_document_modified_added_word(mock_client, tmp_path):
    """Test upsert when document was modified (word added) - should update."""
    # Create a modified version of the test doc with a word added
    modified_doc = tmp_path / "test_upsert_doc.txt"
    modified_doc.write_text("This is a test document for comprehensive upsert testing.\nIt contains a few lines to verify the upsert functionality.\nLine three.\nExtra line added.\n")
    
    # Original size (from the actual test file)
    original_size = len(Path(__file__).parent.joinpath("test_upsert_doc.txt").read_bytes())
    
    with patch.object(mock_client, "find_document_by_file_name", new_callable=AsyncMock) as mock_find, \
         patch.object(mock_client, "upload_file", new_callable=AsyncMock) as mock_upload, \
         patch.object(mock_client, "delete_by_doc", new_callable=AsyncMock) as mock_delete:
        
        # Document exists but with different content length (original was shorter)
        mock_find.return_value = MockExistingDoc(
            doc_id="doc-789",
            content_length=original_size,  # Different from modified file
            file_path="/inputs/test_upsert_doc.txt"
        )
        mock_delete.return_value = {"status": "deleted"}
        mock_upload.return_value = {"status": "success"}
        
        result = await mock_client.upsert_document(modified_doc)
        
        assert result["action"] == "updated"
        assert result["old_doc_id"] == "doc-789"
        mock_find.assert_called_once()
        mock_delete.assert_called_once_with("doc-789")
        mock_upload.assert_called_once_with(modified_doc)


@pytest.mark.asyncio
async def test_upsert_document_file_not_found(mock_client):
    """Test upsert with non-existent file - should raise ResourceNotFoundError."""
    from mcp_lightrag.exceptions import ResourceNotFoundError
    
    with pytest.raises(ResourceNotFoundError):
        await mock_client.upsert_document("/non/existent/file.txt")
