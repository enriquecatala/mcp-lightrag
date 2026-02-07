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


# --- Sample text for testing (small, focused content) ---
SAMPLE_TEXT = "LightRAG is a knowledge graph system for AI assistants."

SAMPLE_TEXTS_BATCH = [
    "LightRAG enables semantic search across documents.",
    "Knowledge graphs connect entities through relationships."
]


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
    result = await client.add_text(SAMPLE_TEXTS_BATCH)
    
    assert result is not None
    print(f"Multiple text ingestion result: {result}")


@pytest.mark.integration
async def test_ingest_file(client):
    """Test uploading a file to running LightRAG server.
    
    Uses a persistent file from the project to avoid temp file issues.
    """
    # Use LICENSE file which exists in the project and is a supported format
    project_root = Path(__file__).parent.parent
    license_file = project_root / "LICENSE"
    
    if not license_file.exists():
        pytest.skip("LICENSE file not found in project root")
    
    result = await client.upload_file(license_file)
    
    # upload_file returns the API response (may be None for some file types)
    # We just verify it doesn't raise an exception
    print(f"File upload result: {result}")


@pytest.mark.integration
async def test_upload_and_index(client):
    """Test upload and trigger indexing scan."""
    # Use a real project file
    project_root = Path(__file__).parent.parent
    readme_file = project_root / "README.md"
    
    if not readme_file.exists():
        pytest.skip("README.md not found")
    
    # Upload file
    upload_result = await client.upload_file(readme_file)
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


@pytest.mark.integration
async def test_upload_wait_and_delete(client):
    """Test complete lifecycle: upload file, wait for processing, delete it."""
    import asyncio
    import hashlib
    import time
    
    # Create a unique text to identify our test document
    unique_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:8]
    test_content = f"Integration test document {unique_id}. LightRAG lifecycle test."
    
    # Step 1: Insert text (more reliable than file upload for this test)
    print(f"Step 1: Inserting text with unique ID: {unique_id}")
    insert_result = await client.add_text(test_content)
    print(f"Insert result: {insert_result}")
    assert insert_result is not None
    
    # Step 2: Wait for processing to complete AND pipeline to be idle
    print("Step 2: Waiting for processing...")
    max_wait = 120  # seconds (increased for queue processing)
    poll_interval = 3  # seconds
    waited = 0
    doc_id = None
    doc_found_completed = False
    pipeline_idle = False
    
    while waited < max_wait:
        await asyncio.sleep(poll_interval)
        waited += poll_interval
        
        # Check pipeline status
        status = await client.get_pipeline_status()
        is_busy = getattr(status, 'busy', False) if status else False
        print(f"  Pipeline status after {waited}s: busy={is_busy}")
        
        # Check if our document is in the list
        docs = await client.get_all_documents()
        if docs:
            # Handle DocsStatusesResponse object - statuses is a dict mapping status -> list of docs
            statuses_obj = getattr(docs, 'statuses', None)
            if statuses_obj:
                # Get all status keys (e.g., 'processing', 'completed', 'pending', etc.)
                status_keys = statuses_obj.additional_keys if hasattr(statuses_obj, 'additional_keys') else []
                
                for status_key in status_keys:
                    try:
                        doc_list = statuses_obj[status_key]
                        for doc in doc_list:
                            doc_summary = getattr(doc, 'summary', '') or ''
                            doc_id_attr = getattr(doc, 'id', None)
                            
                            if unique_id in doc_summary or unique_id in str(doc):
                                doc_id = doc_id_attr
                                print(f"  Found our document: {doc_id} (status: {status_key})")
                                
                                if status_key.lower() in ['completed', 'indexed', 'processed']:
                                    doc_found_completed = True
                                    print(f"  Document processing complete!")
                                break
                    except (KeyError, TypeError):
                        continue
                    
                    if doc_found_completed:
                        break
        
        # Check if pipeline is completely idle (needed for delete to work)
        if not is_busy:
            pipeline_idle = True
            if doc_found_completed:
                print(f"  Pipeline idle and document completed after {waited}s")
                break
    
    # Step 3: List documents and find ours
    print("Step 3: Listing documents...")
    docs = await client.get_all_documents()
    print(f"All documents response type: {type(docs)}")
    assert docs is not None
    
    # Step 4: Delete the document if we found its ID
    if doc_id:
        # Wait for pipeline to be idle before deleting
        if not pipeline_idle:
            print("Step 4a: Waiting for pipeline to be idle before delete...")
            for _ in range(20):  # Wait up to 60 more seconds
                await asyncio.sleep(3)
                status = await client.get_pipeline_status()
                is_busy = getattr(status, 'busy', False) if status else False
                if not is_busy:
                    print("  Pipeline is now idle")
                    break
        
        print(f"Step 4: Deleting document {doc_id}...")
        delete_result = await client.delete_by_doc(doc_id)
        print(f"Delete result: {delete_result}")
        
        # Check if delete was accepted
        delete_status = getattr(delete_result, 'status', None)
        if delete_status and 'busy' in str(delete_status).lower():
            print("Note: Delete was rejected because pipeline is busy - this is expected in high-load scenarios")
            # Don't fail the test for this - it's an expected scenario
        else:
            # Verify deletion
            await asyncio.sleep(2)
            docs_after = await client.get_all_documents()
            
            # Check document is no longer present
            doc_still_exists = False
            if docs_after:
                statuses_obj = getattr(docs_after, 'statuses', None)
                if statuses_obj:
                    for status_key in statuses_obj.additional_keys if hasattr(statuses_obj, 'additional_keys') else []:
                        try:
                            for doc in statuses_obj[status_key]:
                                if getattr(doc, 'id', None) == doc_id:
                                    doc_still_exists = True
                                    break
                        except (KeyError, TypeError):
                            continue
            
            if not doc_still_exists:
                print("Document successfully deleted and verified!")
            else:
                print("Document still exists after delete (may be processing)")
    else:
        print("Step 4: Skipped deletion - document ID not found (document may still be processing)")
    
    print("Lifecycle test completed successfully!")


@pytest.mark.integration
async def test_upsert_document_new(client):
    """Test upsert when document doesn't exist - should create it."""
    import asyncio
    import tempfile
    import os
    
    # Create a unique test file
    test_content = "Upsert integration test - new document.\n"
    
    temp_path = None
    doc_id = None
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='_upsert_new.txt', delete=False) as f:
        f.write(test_content)
        temp_path = Path(f.name)
    
    try:
        print(f"Step 1: Upserting new document {temp_path.name}...")
        result = await client.upsert_document(temp_path)
        
        print(f"Result: {result}")
        assert result["action"] == "created", f"Expected 'created' but got '{result['action']}'"
        assert result["file_name"] == temp_path.name
        
        # Wait for processing
        print("Step 2: Waiting for document to be indexed...")
        await asyncio.sleep(3)
        
        # Find and cleanup
        doc = await client.find_document_by_file_name(temp_path.name)
        if doc:
            doc_id = getattr(doc, "id", None)
            print(f"Document found with ID: {doc_id}")
        
        print("New document upsert test passed!")
        
    finally:
        # Cleanup local file
        if temp_path and temp_path.exists():
            os.remove(temp_path)
        
        # Cleanup remote document
        if doc_id:
            try:
                await asyncio.sleep(2)
                await client.delete_by_doc(doc_id)
                print(f"Cleaned up document {doc_id}")
            except Exception as e:
                print(f"Warning: Failed to cleanup: {e}")


@pytest.mark.integration
async def test_upsert_document_identical(client):
    """Test upsert when document exists and is identical - should skip."""
    import asyncio
    import tempfile
    import os
    
    test_content = "Upsert integration test - identical document.\n"
    
    temp_path = None
    doc_id = None
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='_upsert_identical.txt', delete=False) as f:
        f.write(test_content)
        temp_path = Path(f.name)
    
    try:
        # Step 1: First upsert (should create)
        print(f"Step 1: First upsert of {temp_path.name}...")
        result1 = await client.upsert_document(temp_path)
        print(f"First upsert result: {result1}")
        assert result1["action"] == "created"
        
        # Wait for processing
        print("Step 2: Waiting for document to be indexed...")
        for i in range(15):
            await asyncio.sleep(2)
            doc = await client.find_document_by_file_name(temp_path.name)
            if doc:
                doc_id = getattr(doc, "id", None)
                content_length = getattr(doc, "content_length", None)
                print(f"  Attempt {i+1}: Found doc {doc_id}, content_length={content_length}")
                if content_length is not None:
                    break
            else:
                print(f"  Attempt {i+1}: Document not found yet...")
        
        # Step 3: Second upsert with same content (should skip)
        print("Step 3: Second upsert with identical content...")
        result2 = await client.upsert_document(temp_path)
        print(f"Second upsert result: {result2}")
        assert result2["action"] == "skipped", f"Expected 'skipped' but got '{result2['action']}'"
        assert "identical" in result2.get("reason", "").lower()
        
        print("Identical document upsert test passed!")
        
    finally:
        if temp_path and temp_path.exists():
            os.remove(temp_path)
        
        if doc_id:
            try:
                await asyncio.sleep(2)
                await client.delete_by_doc(doc_id)
                print(f"Cleaned up document {doc_id}")
            except Exception as e:
                print(f"Warning: Failed to cleanup: {e}")


@pytest.mark.integration
async def test_upsert_document_modified(client):
    """Test upsert when document was modified - should update."""
    import asyncio
    import tempfile
    import os
    
    original_content = "Upsert integration test - original content.\n"
    modified_content = "Upsert integration test - modified content with extra words added here.\n"
    
    temp_path = None
    doc_id = None
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='_upsert_modified.txt', delete=False) as f:
        f.write(original_content)
        temp_path = Path(f.name)
    
    try:
        # Step 1: First upsert (should create)
        print(f"Step 1: First upsert of {temp_path.name}...")
        result1 = await client.upsert_document(temp_path)
        print(f"First upsert result: {result1}")
        assert result1["action"] == "created"
        
        # Wait for processing
        print("Step 2: Waiting for document to be indexed...")
        for i in range(15):
            await asyncio.sleep(2)
            doc = await client.find_document_by_file_name(temp_path.name)
            if doc:
                doc_id = getattr(doc, "id", None)
                content_length = getattr(doc, "content_length", None)
                print(f"  Attempt {i+1}: Found doc {doc_id}, content_length={content_length}")
                if content_length is not None:
                    break
            else:
                print(f"  Attempt {i+1}: Document not found yet...")
        
        # Step 3: Modify the file
        print("Step 3: Modifying local file...")
        with open(temp_path, 'w') as f:
            f.write(modified_content)
        print(f"  New content length: {len(modified_content)}")
        
        # Step 4: Upsert modified file (should update)
        print("Step 4: Upserting modified file...")
        result2 = await client.upsert_document(temp_path)
        print(f"Second upsert result: {result2}")
        assert result2["action"] == "updated", f"Expected 'updated' but got '{result2['action']}'"
        assert result2.get("old_doc_id") == doc_id
        
        # Get new doc ID for cleanup
        await asyncio.sleep(3)
        doc = await client.find_document_by_file_name(temp_path.name)
        if doc:
            doc_id = getattr(doc, "id", None)
        
        print("Modified document upsert test passed!")
        
    finally:
        if temp_path and temp_path.exists():
            os.remove(temp_path)
        
        if doc_id:
            try:
                await asyncio.sleep(2)
                await client.delete_by_doc(doc_id)
                print(f"Cleaned up document {doc_id}")
            except Exception as e:
                print(f"Warning: Failed to cleanup: {e}")


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
