"""
API client for LightRAG with robust error handling and retries.
"""

import asyncio
import logging
import re
import functools
from pathlib import Path
from typing import Any, Awaitable, Callable, Dict, List, Optional, TypeVar, Union

import httpx
from .exceptions import (
    APIConnectionError, 
    APIResponseError, 
    ResourceNotFoundError
)
from .models import ServerSettings

# Import auto-generated client components
from .client.light_rag_server_api_client.client import AuthenticatedClient

# Default
from .client.light_rag_server_api_client.api.default.get_status_health_get import asyncio as async_get_health

# Documents
from .client.light_rag_server_api_client.api.documents.documents_documents_get import asyncio as async_get_documents
from .client.light_rag_server_api_client.api.documents.get_pipeline_status_documents_pipeline_status_get import asyncio as async_get_pipeline_status
from .client.light_rag_server_api_client.api.documents.insert_text_documents_text_post import asyncio as async_insert_document
from .client.light_rag_server_api_client.api.documents.insert_texts_documents_texts_post import asyncio as async_insert_texts
from .client.light_rag_server_api_client.api.documents.scan_for_new_documents_documents_scan_post import asyncio as async_scan_for_new_documents
from .client.light_rag_server_api_client.api.documents.upload_to_input_dir_documents_upload_post import asyncio as async_upload_document
from .client.light_rag_server_api_client.api.documents.delete_document_documents_delete_document_delete import asyncio as async_delete_by_doc_id
from .client.light_rag_server_api_client.api.documents.delete_entity_documents_delete_entity_delete import asyncio as async_delete_entity


# Graph
from .client.light_rag_server_api_client.api.graph.create_entity_graph_entity_create_post import asyncio as async_create_entity
from .client.light_rag_server_api_client.api.graph.create_relation_graph_relation_create_post import asyncio as async_create_relation
from .client.light_rag_server_api_client.api.graph.update_entity_graph_entity_edit_post import asyncio as async_edit_entity
from .client.light_rag_server_api_client.api.graph.update_relation_graph_relation_edit_post import asyncio as async_edit_relation
from .client.light_rag_server_api_client.api.graph.get_graph_labels_graph_label_list_get import asyncio as async_get_graph_labels
from .client.light_rag_server_api_client.api.graph.merge_entities_graph_entities_merge_post import asyncio as async_merge_entities

# Query
from .client.light_rag_server_api_client.api.query.query_text_query_post import asyncio as async_query_document

from .client.light_rag_server_api_client.models import (
    BodyUploadToInputDirDocumentsUploadPost,
    InsertTextRequest,
    InsertTextsRequest,
    QueryRequest,
    EntityMergeRequest as MergeEntitiesRequest,
    EntityCreateRequest,
    EntityCreateRequestEntityData,
    EntityUpdateRequest,
    EntityUpdateRequestUpdatedData,
    RelationCreateRequest,
    RelationCreateRequestRelationData,
    RelationUpdateRequest,
    RelationUpdateRequestUpdatedData,
    DeleteDocRequest,
    DeleteEntityRequest,
    DocumentsRequest,
    DocumentsRequestSortField,
    DocumentsRequestSortDirection,
)

from .client.light_rag_server_api_client.api.documents.get_documents_paginated_documents_paginated_post import asyncio as async_get_documents_paginated
from .client.light_rag_server_api_client.types import File
from .client.light_rag_server_api_client.errors import UnexpectedStatus

logger = logging.getLogger(__name__)

T = TypeVar("T")

def with_retry(max_retries: int = 3, base_delay: float = 1.0):
    """
    Decorator for async methods to implement exponential backoff retry logic.
    """
    def decorator(func: Callable[..., Awaitable[T]]):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries):
                try:
                    return await func(*args, **kwargs)
                except (httpx.ConnectError, httpx.TimeoutException, UnexpectedStatus) as e:
                    last_exception = e
                    # Don't retry on certain status codes if it's an UnexpectedStatus
                    if isinstance(e, UnexpectedStatus) and e.status_code in [400, 401, 403, 404]:
                        raise
                    
                    delay = base_delay * (2 ** attempt)
                    logger.warning(
                        f"Attempt {attempt + 1} failed for {func.__name__}: {str(e)}. "
                        f"Retrying in {delay:.2f}s..."
                    )
                    await asyncio.sleep(delay)
            
            logger.error(f"All {max_retries} attempts failed for {func.__name__}")
            raise last_exception
        return wrapper
    return decorator

class LightRAGApiClient:
    """
    Client for interacting with the LightRAG API.
    """

    def __init__(self, settings: ServerSettings):
        """
        Initialize the client with provided settings.
        """
        self.settings = settings
        # Use AuthenticatedClient only if api_key is provided, otherwise use Client
        # This avoids sending invalid 'Bearer ' header when auth is disabled
        if settings.api_key:
            self.client = AuthenticatedClient(
                base_url=settings.base_url, 
                token=settings.api_key, 
                verify_ssl=False
            )
        else:
            from .client.light_rag_server_api_client.client import Client
            self.client = Client(
                base_url=settings.base_url,
                verify_ssl=False
            )
        logger.info(f"Connected to LightRAG API at {settings.base_url}")

    async def close(self):
        """Clean up resources."""
        await self.client.get_async_httpx_client().aclose()
        logger.debug("API client connection closed")

    @with_retry()
    async def _execute_op(self, api_func, name: str, **kwargs) -> Any:
        """Helper to execute API operations with logging and retries."""
        try:
            logger.debug(f"Starting operation: {name}")
            result = await api_func(client=self.client, **kwargs)
            return result
        except UnexpectedStatus as e:
            logger.error(f"API Error ({name}): {e.status_code} - {e.content!r}")
            raise APIResponseError(f"API operation '{name}' failed", status_code=e.status_code, details=str(e.content))
        except Exception as e:
            logger.error(f"Unexpected error during {name}: {str(e)}")
            raise APIConnectionError(f"Failed to connect for '{name}'") from e

    # --- Document Operations ---

    async def query(self, params: 'QueryRequest') -> Any:
        """Perform a knowledge graph query."""
        return await self._execute_op(async_query_document, "query", body=params)

    async def add_text(self, text: Union[str, List[str]]) -> Any:
        """Insert text content into the graph."""
        if isinstance(text, str):
            request = InsertTextRequest(text=text)
            return await self._execute_op(async_insert_document, "insert_text", body=request)
        else:
            request = InsertTextsRequest(texts=text)
            return await self._execute_op(async_insert_texts, "insert_texts", body=request)

    async def upload_file(self, file_path: Union[str, Path]) -> Any:
        """Upload a file to the inputs directory for processing."""
        path = Path(file_path)
        if not path.exists():
            raise ResourceNotFoundError(f"File not found: {file_path}")
            
        with open(path, "rb") as f:
            request = BodyUploadToInputDirDocumentsUploadPost(
                file=File(payload=f, file_name=path.name)
            )
            return await self._execute_op(async_upload_document, f"upload_{path.name}", body=request)

    async def index_file(self, file_path: Union[str, Path]) -> Any:
        """Directly index a local file.
           Deprecated: Use upload_file instead as direct indexing is no longer supported.
        """
        # Fallback to upload_file since insert_file is removed
        return await self.upload_file(file_path)

    async def get_all_documents(self) -> Any:
        """Retrieve list of all indexed documents."""
        # Use paginated API to fetch all documents if possible, or fallback to legacy endpoint
        # The legacy endpoint is deprecated and limited to 1000 docs
        return await self._execute_op(async_get_documents, "list_documents")

    async def get_documents_paginated(
        self, 
        page: int = 1, 
        page_size: int = 50,
        sort_field: str = "updated_at",
        sort_direction: str = "desc",
        status_filter: Optional[str] = None
    ) -> Any:
        """Retrieve documents with pagination."""
        request = DocumentsRequest(
            page=page,
            page_size=page_size,
            sort_field=DocumentsRequestSortField(sort_field),
            sort_direction=DocumentsRequestSortDirection(sort_direction),
            status_filter=status_filter or None
        )
        return await self._execute_op(async_get_documents_paginated, "list_documents_paginated", body=request)

    async def find_document_by_file_name(self, file_name: str) -> Optional[Any]:
        """
        Find a document by its file name or path.
        Returns the document DocStatusResponse object if found, None otherwise.
        
        This method iterates through paginated results to find the document.
        """
        page = 1
        page_size = 100
        
        while True:
            response = await self.get_documents_paginated(page=page, page_size=page_size)
            
            # Handle response structure
            if not response:
                break
                
            docs = getattr(response, "documents", [])
            
            # Access pagination object properties correctly
            pagination = getattr(response, "pagination", None)
            total_count = getattr(pagination, "total_count", 0) if pagination else 0
            
            # Check current page
            for doc in docs:
                doc_path = getattr(doc, "file_path", "") or ""
                doc_name = Path(doc_path).name
                
                # Check for exact match on full path or filename
                if file_name == doc_path or file_name == doc_name:
                    return doc
                
                # Only log if check fails
                # logger.debug(f"Checking doc: {doc_path} ({doc_name}) vs {file_name}")
            
            # Check if we need to fetch next page
            if (page * page_size) >= total_count or not docs:
                break
                
            page += 1
            
        return None

    async def get_pipeline_status(self) -> Any:
        """Check the status of the indexing pipeline."""
        return await self._execute_op(async_get_pipeline_status, "pipeline_status")

    async def scan_inputs(self) -> Any:
        """Trigger a scan for new files in the inputs directory."""
        return await self._execute_op(async_scan_for_new_documents, "scan_inputs")

    async def ingest_batch(
        self,
        directory: Union[str, Path],
        recursive: bool = False,
        depth: int = 1,
        include_only: List[str] = None,
        ignore_files: List[str] = None,
        ignore_dirs: List[str] = None
    ) -> Dict[str, Any]:
        """Index a collection of files from a directory."""
        dir_path = Path(directory)
        if not dir_path.exists() or not dir_path.is_dir():
            raise ResourceNotFoundError(f"Directory not found: {directory}")

        include_re = [re.compile(p) for p in (include_only or [])]
        ignore_file_re = [re.compile(p) for p in (ignore_files or [])]
        ignore_dir_re = [re.compile(p) for p in (ignore_dirs or [])]

        def should_include(p: Path) -> bool:
            if include_re:
                return any(r.search(p.name) for r in include_re)
            if ignore_file_re:
                return not any(r.search(p.name) for r in ignore_file_re)
            return True

        def should_ignore_dir(p: Path) -> bool:
            return any(r.search(p.name) for r in ignore_dir_re)

        files_to_process = []

        def collect(curr_dir: Path, curr_depth: int):
            for item in curr_dir.iterdir():
                if item.is_dir() and recursive and curr_depth < depth:
                    if not should_ignore_dir(item):
                        collect(item, curr_depth + 1)
                elif item.is_file():
                    if should_include(item):
                        files_to_process.append(item)

        collect(dir_path, 0)
        logger.info(f"Found {len(files_to_process)} files in {directory}")

        results = []
        for f in files_to_process:
            try:
                await self.index_file(f)
                results.append({"file": str(f), "status": "ok"})
            except Exception as e:
                results.append({"file": str(f), "status": "fail", "error": str(e)})

        return {
            "total": len(files_to_process),
            "successful": sum(1 for r in results if r['status'] == 'ok'),
            "failed": sum(1 for r in results if r['status'] == 'fail'),
            "details": results
        }

    # --- Graph Operations ---

    async def get_labels(self) -> Any:
        """Get labels from the knowledge graph."""
        return await self._execute_op(async_get_graph_labels, "get_labels")

    async def create_entity(self, name: str, type: str, description: str, source_id: str) -> Any:
        """Add a new entity to the knowledge graph."""
        data = EntityCreateRequestEntityData.from_dict({
            "entity_type": type, 
            "description": description, 
            "source_id": source_id
        })
        body = EntityCreateRequest(entity_name=name, entity_data=data)
        return await self._execute_op(async_create_entity, f"create_entity_{name}", body=body)

    async def delete_entity(self, name: str) -> Any:
        """Remove an entity from the knowledge graph."""
        body = DeleteEntityRequest(entity_name=name)
        return await self._execute_op(async_delete_entity, f"delete_entity_{name}", body=body)

    async def delete_by_doc(self, doc_id: str) -> Any:
        """Remove all graph elements associated with a document ID."""
        body = DeleteDocRequest(doc_ids=[doc_id])
        return await self._execute_op(async_delete_by_doc_id, f"delete_doc_{doc_id}", body=body)

    async def edit_entity(self, name: str, type: str, description: str, source_id: str) -> Any:
        """Update an existing entity."""
        data = EntityUpdateRequestUpdatedData.from_dict({
            "entity_type": type, 
            "description": description, 
            "source_id": source_id
        })
        body = EntityUpdateRequest(entity_name=name, updated_data=data)
        return await self._execute_op(async_edit_entity, f"edit_entity_{name}", body=body)

    async def merge_entities(self, sources: List[str], target: str, strategy: Dict[str, str]) -> Any:
        """Merge multiple entities into a single target entity."""
        # Strategy argument is kept for API compatibility but ignored as the server API handles it differently now
        body = MergeEntitiesRequest(
            entities_to_change=sources,
            entity_to_change_into=target
        )
        return await self._execute_op(async_merge_entities, f"merge_to_{target}", body=body)

    async def manage_relation(self, source: str, target: str, description: str, keywords: str, 
                               relation_type: Optional[str] = None, source_id: Optional[str] = None, 
                               weight: Optional[float] = None, is_edit: bool = False) -> Any:
        """Create or update a relationship between entities."""
        
        if is_edit:
            data = RelationUpdateRequestUpdatedData.from_dict({
                "description": description,
                "keywords": keywords,
                "weight": weight
            })
            body = RelationUpdateRequest(
                source_entity=source,
                target_entity=target,
                updated_data=data
            )
            return await self._execute_op(
                async_edit_relation, 
                f"edit_rel_{source}_{target}", 
                body=body
            )
        else:
            data = RelationCreateRequestRelationData.from_dict({
                "description": description,
                "keywords": keywords,
                "weight": weight,
                "source_id": source_id
            })
            body = RelationCreateRequest(
                source_entity=source,
                target_entity=target,
                relation_data=data
            )
            return await self._execute_op(
                async_create_relation, 
                f"create_rel_{source}_{target}", 
                body=body
            )

    async def check_health(self) -> Any:
        """Check if the LightRAG service is healthy."""
        return await self._execute_op(async_get_health, "health_check")
