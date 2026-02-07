
import pytest
from pathlib import Path
from dotenv import load_dotenv

from mcp_lightrag.api_client import LightRAGApiClient
from mcp_lightrag.models import ServerSettings

# Load environment variables from .env file
load_dotenv()

@pytest.fixture
def client_settings():
    return ServerSettings(
        host="localhost",
        port=9621,
    )

@pytest.fixture
async def client(client_settings):
    api_client = LightRAGApiClient(client_settings)
    yield api_client
    await api_client.close()

@pytest.mark.integration
@pytest.mark.asyncio
async def test_find_document_by_file_name(client):
    """Test finding a document by its file name using the paginated search helper."""

    # First test with a known existing file if possible (e.g. README.md from previous tests)
    # This verifies the method works at all
    print("Searching for potentially existing README.md...")
    readme_doc = await client.find_document_by_file_name("README.md")
    if readme_doc:
        print("Found README.md! Method works.")
    else:
        print("README.md not found (might not be indexed yet).")

    # Use a file that is likely to exist or upload one
    test_filename = "test_find_doc.txt"
    test_content = "This is a test document for finding by filename."
    
    # Let's create a real file to upload so it has a path
    import tempfile
    import os
    
    temp_path = None
    doc = None
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(test_content)
        temp_path = f.name
        
    try:
        # Upload
        print(f"Uploading {temp_path}...")
        await client.upload_file(temp_path)
        
        # Trigger scan to ensure processing starts immediately
        await client.scan_inputs()
        
        # Determine the name we expect to find
        expected_name = Path(temp_path).name
        
        # Wait slightly for processing to register
        import asyncio
        await asyncio.sleep(1)
        
        # Find the document with retry
        print(f"Searching for document: {expected_name}")
        doc = None
        for i in range(10):
            doc = await client.find_document_by_file_name(expected_name)
            if doc:
                break
            print(f"  Attempt {i+1}: Document not found yet, waiting...")
            await asyncio.sleep(2)
        
        assert doc is not None, f"Document {expected_name} not found after retries"
        
        # Verify details
        doc_path = getattr(doc, "file_path", "")
        # doc.id is usually doc_id attribute on the model
        doc_id = getattr(doc, "id", "unknown")
        print(f"Found document: id={doc_id}, path={doc_path}")
        assert expected_name in doc_path
        
    finally:
        # Cleanup local file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
            
        # Delete from LightRAG if found to keep environment clean
        if doc:
            doc_id = getattr(doc, "id", None)
            if doc_id:
                try:
                    await client.delete_by_doc(doc_id)
                    print(f"Cleaned up document {doc_id}")
                except Exception as e:
                    print(f"Warning: Failed to cleanup document {doc_id}: {e}")

@pytest.mark.integration
@pytest.mark.asyncio
async def test_pagination(client):
    """Test retrieving documents with pagination."""
    # Use page_size=10 as minimum required by API
    response = await client.get_documents_paginated(page=1, page_size=10)
    
    assert response is not None
    
    pagination = getattr(response, "pagination", None)
    assert pagination is not None
    
    total_count = getattr(pagination, "total_count", 0)
    print(f"Total documents: {total_count}")
    
    docs = getattr(response, "documents", [])
    print(f"Docs on page 1: {len(docs)}")
    
    if total_count > 10:
        # Fetch page 2
        response2 = await client.get_documents_paginated(page=2, page_size=10)
        docs2 = getattr(response2, "documents", [])
        print(f"Docs on page 2: {len(docs2)}")
        assert len(docs2) > 0
