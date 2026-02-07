
import pytest
from unittest.mock import AsyncMock, MagicMock
from mcp.server.fastmcp import Context

from mcp_lightrag.mcp_tools import list_all_docs, AppContext

@pytest.fixture
def mock_context():
    # Create a mock for the Context object
    ctx = MagicMock(spec=Context)
    
    # Create a mock for the API client
    mock_api = AsyncMock()
    
    # Create a mock for the AppContext that holds the API client
    app_context = MagicMock(spec=AppContext)
    app_context.api = mock_api
    
    # Set up the context structure: ctx.request_context.lifespan_context
    ctx.request_context = MagicMock()
    ctx.request_context.lifespan_context = app_context
    
    return ctx, mock_api

@pytest.mark.asyncio
async def test_list_all_docs(mock_context):
    ctx, mock_api = mock_context
    
    # Define the expected return value from the API client
    expected_docs = [{"id": "doc1", "title": "Test Doc"}]
    mock_api.get_all_documents.return_value = expected_docs
    
    # Call the tool function
    result = await list_all_docs(ctx)
    
    # Verify the API client was called correctly
    mock_api.get_all_documents.assert_called_once()
    
    # Verify the result format (wrapped in OperationResult by @format_output decorator)
    assert result["status"] == "success"
    assert result["response"] == expected_docs
