"""
MCP tool definitions for LightRAG server.
"""

import functools
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Union, cast

from mcp.server.fastmcp import Context, FastMCP
from pydantic import Field

from .api_client import LightRAGApiClient
from .settings import get_settings
from .models import OperationResult, BatchResult
from .client.light_rag_server_api_client.models import QueryRequest, QueryRequestMode

logger = logging.getLogger(__name__)

class AppContext:
    """Type-safe application context."""
    def __init__(self, client: LightRAGApiClient):
        self.api = client

@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manages the lifecycle of the API client."""
    # Re-fetch settings here to capture any environment variable overrides from CLI
    client = LightRAGApiClient(get_settings())
    try:
        yield AppContext(client)
    finally:
        await client.close()
        logger.info("LightRAG MCP service shut down")

# Initialize FastMCP with lifespan management
mcp = FastMCP("LightRAG-Server", lifespan=lifespan)

def format_output(func):
    """Decorator to standardize tool responses."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return OperationResult.success(result).__dict__
        except Exception as e:
            logger.exception(f"Tool execution failed: {str(e)}")
            return OperationResult.failure(str(e)).__dict__
    return wrapper

async def get_api(ctx: Context) -> LightRAGApiClient:
    """Helper to extract the API client from MCP context."""
    if not ctx or not ctx.request_context or not ctx.request_context.lifespan_context:
        raise RuntimeError("Application context not initialized")
    return cast(AppContext, ctx.request_context.lifespan_context).api

# --- Search & Query Tools ---

@mcp.tool(name="query_knowledge_graph", description="Search the knowledge graph for information using various strategies. Ideal for answering questions based on indexed data.")
@format_output
async def query_knowledge_graph(
    ctx: Context,
    prompt: str = Field(description="The question or search query to execute against the knowledge base"),
    search_mode: str = Field(
        description="Search strategy to use: 'mix' (recommended for comprehensive results), 'semantic' (vector search), 'keyword' (exact match), 'global' (broad context), 'hybrid' (semantic + keyword), 'local' (specific context), 'naive' (simple)",
        default="mix"
    ),
    limit: int = Field(description="Maximum number of result items/paragraphs to retrieve", default=60),
    context_only: bool = Field(description="If True, returns only the raw context data without LLM generation", default=False),
    prompt_only: bool = Field(description="If True, returns only the constructed LLM prompt without executing it to the LLM", default=False),
) -> Any:
    """Execute a RAG query against the knowledge graph."""
    api = await get_api(ctx)
    params = QueryRequest(
        query=prompt,
        mode=QueryRequestMode(search_mode),
        top_k=limit,
        only_need_context=context_only,
        only_need_prompt=prompt_only,
        # Sensible defaults for other params
        response_type="Multiple Paragraphs",
        max_token_for_text_unit=4096,
        max_token_for_global_context=4096,
        max_token_for_local_context=4096,
        history_turns=10
    )
    return await api.query(params)

# --- Document Management Tools ---

@mcp.tool(name="ingest_text", description="Index raw text content directly into the knowledge graph. Useful for small snippets or dynamic data.")
@format_output
async def ingest_text(
    ctx: Context,
    content: Union[str, List[str]] = Field(description="The text content (string or list of strings) to be indexed")
) -> Any:
    api = await get_api(ctx)
    return await api.add_text(content)

@mcp.tool(name="ingest_file", description="Index a specific local file from the file system. The file must be accessible by the running server.")
@format_output
async def ingest_file(
    ctx: Context,
    file_path: str = Field(description="Absolute path to the local file to be indexed")
) -> Any:
    api = await get_api(ctx)
    return await api.index_file(file_path)

@mcp.tool(name="upload_and_index", description="Upload a file to the LightRAG server's input directory and trigger indexing. Handles file transfer if the server is remote.")
@format_output
async def upload_and_index(
    ctx: Context,
    file_path: str = Field(description="Local path to the file to upload and index")
) -> Any:
    api = await get_api(ctx)
    return await api.upload_file(file_path)

@mcp.tool(name="upsert_document", description="Intelligently upload a document: if it doesn't exist, creates it; if it exists and is identical (same content length), skips upload; if it exists but was modified, deletes the old version and re-uploads.")
@format_output
async def upsert_document(
    ctx: Context,
    file_path: str = Field(description="Local path to the document file to upsert")
) -> Any:
    """
    Smart document upload that handles three scenarios:
    - NEW: Document doesn't exist → uploads it
    - IDENTICAL: Document exists with same content → skips (returns success)
    - MODIFIED: Document exists but content changed → deletes old, uploads new
    """
    api = await get_api(ctx)
    return await api.upsert_document(file_path)


@mcp.tool(name="ingest_batch", description="Recursively index all files in a directory that match specific patterns.")
@format_output
async def ingest_batch(
    ctx: Context,
    directory_path: str = Field(description="Absolute path to the directory to scan"),
    recursive: bool = Field(description="If True, scans subdirectories recursively", default=False),
    max_depth: int = Field(description="Maximum depth for recursive scanning", default=1),
    include_patterns: List[str] = Field(description="List of glob patterns for files to include (e.g. ['*.txt', '*.md'])", default_factory=list),
    ignore_patterns: List[str] = Field(description="List of glob patterns for files to exclude", default_factory=list)
) -> Any:
    api = await get_api(ctx)
    return await api.ingest_batch(
        directory=directory_path,
        recursive=recursive,
        depth=max_depth,
        include_only=include_patterns,
        ignore_files=ignore_patterns
    )

@mcp.tool(name="list_all_docs", description="List ALL documents currently in the system. WARNING: Can be slow if there are many documents. Use get_latest_documents for better performance.")
@format_output
async def list_all_docs(ctx: Context) -> Any:
    api = await get_api(ctx)
    return await api.get_all_documents()

@mcp.tool(name="find_document", description="Check if a document exists by its filename or path. Returns a dictionary with detailed status: 'id', 'status' (processed/failed/pending), 'created_at', 'updated_at', 'content_length', 'chunks_count', and 'error_msg' if any.")
@format_output
async def find_document(
    ctx: Context,
    filename: str = Field(description="The name or path of the document file to find (e.g., 'report.pdf')")
) -> Any:
    api = await get_api(ctx)
    doc = await api.find_document_by_file_name(filename)
    if doc and hasattr(doc, "to_dict"):
        return doc.to_dict()
    return doc

@mcp.tool(name="get_latest_documents", description="Get a paginated list of the most recently updated documents. Useful for monitoring ingestion progress.")
@format_output
async def get_latest_documents(
    ctx: Context,
    limit: int = Field(description="Number of documents to retrieve (10-100)", default=10),
    status: str = Field(description="Optional filter by status (e.g. 'processed', 'failed', 'pending')", default=None)
) -> Any:
    api = await get_api(ctx)
    # Ensure limit is within API bounds (10-200)
    limit = max(10, min(limit, 100))
    result = await api.get_documents_paginated(page=1, page_size=limit, sort_field="updated_at", sort_direction="desc", status_filter=status)
    if result and hasattr(result, "to_dict"):
        return result.to_dict()
    return result

@mcp.tool(name="check_indexing_status", description="Check the current status of the document processing pipeline (idle or busy).")
@format_output
async def check_indexing_status(ctx: Context) -> Any:
    api = await get_api(ctx)
    return await api.get_pipeline_status()

# --- Graph Schema & Health ---

@mcp.tool(name="get_graph_metadata", description="Retrieve schema information about the knowledge graph, including available node labels and relationship types.")
@format_output
async def get_graph_metadata(ctx: Context) -> Any:
    api = await get_api(ctx)
    return await api.get_labels()

@mcp.tool(name="verify_server_health", description="Check if the LightRAG server is reachable and healthy.")
@format_output
async def verify_server_health(ctx: Context) -> Any:
    api = await get_api(ctx)
    return await api.check_health()

# --- Entity & Relationship Management ---

@mcp.tool(name="create_entities", description="Manually insert specific entities into the knowledge graph.")
@format_output
async def create_entities(
    ctx: Context,
    entities: List[Dict[str, Any]] = Field(description="List of entity dictionaries. Each must contain: 'name', 'type', 'description', 'source_id'")
) -> Any:
    api = await get_api(ctx)
    results = []
    for e in entities:
        try:
            res = await api.create_entity(
                name=str(e['name']), 
                type=str(e['type']), 
                description=str(e['description']), 
                source_id=str(e['source_id'])
            )
            results.append({"name": e['name'], "status": "ok", "data": res})
        except Exception as err:
            results.append({"name": e.get('name', 'unknown'), "status": "fail", "error": str(err)})
    
    return BatchResult(
        total=len(entities),
        successful=sum(1 for r in results if r['status'] == 'ok'),
        failed=sum(1 for r in results if r['status'] == 'fail'),
        results=results
    )

@mcp.tool(name="remove_entities", description="Delete one or more specific entities from the knowledge graph by name.")
@format_output
async def remove_entities(
    ctx: Context,
    names: List[str] = Field(description="List of entity names to delete")
) -> Any:
    api = await get_api(ctx)
    results = []
    for name in names:
        try:
            res = await api.delete_entity(name)
            results.append({"name": name, "status": "ok", "data": res})
        except Exception as err:
            results.append({"name": name, "status": "fail", "error": str(err)})
    return results

@mcp.tool(name="purge_by_document", description="Remove all entities and relationships associated with specific document IDs from the graph.")
@format_output
async def purge_by_document(
    ctx: Context,
    doc_ids: List[str] = Field(description="List of document IDs (e.g., from find_document) to prune from the graph")
) -> Any:
    api = await get_api(ctx)
    results = []
    for doc_id in doc_ids:
        try:
            res = await api.delete_by_doc(doc_id)
            results.append({"id": doc_id, "status": "ok", "data": res})
        except Exception as err:
            results.append({"id": doc_id, "status": "fail", "error": str(err)})
    return results

@mcp.tool(name="modify_entities", description="Update the properties (type, description, source_id) of existing entities.")
@format_output
async def modify_entities(
    ctx: Context,
    entities: List[Dict[str, Any]] = Field(description="List of dictionaries with updated entity fields. Must include 'name'. Optional: 'type', 'description', 'source_id'")
) -> Any:
    api = await get_api(ctx)
    results = []
    for e in entities:
        try:
            res = await api.edit_entity(
                name=str(e['name']),
                type=str(e['type']),
                description=str(e['description']),
                source_id=str(e['source_id'])
            )
            results.append({"name": e['name'], "status": "ok", "data": res})
        except Exception as err:
            results.append({"name": e['name'], "status": "fail", "error": str(err)})
    return results

@mcp.tool(name="connect_entities", description="Define or update relationships between entities, including edge weights and descriptions.")
@format_output
async def connect_entities(
    ctx: Context,
    relations: List[Dict[str, Any]] = Field(description="List of relationship definitions. Required: 'source', 'target'. Optional: 'description', 'keywords', 'weight', 'type', 'edit_mode'")
) -> Any:
    api = await get_api(ctx)
    results = []
    for r in relations:
        try:
            res = await api.manage_relation(
                source=str(r['source']),
                target=str(r['target']),
                description=str(r['description']),
                keywords=str(r['keywords']),
                relation_type=r.get('type'),
                source_id=r.get('source_id'),
                weight=r.get('weight'),
                is_edit=bool(r.get('edit_mode', False))
            )
            results.append({"rel": f"{r['source']}->{r['target']}", "status": "ok", "data": res})
        except Exception as err:
            results.append({"rel": f"{r.get('source')}->{r.get('target')}", "status": "fail", "error": str(err)})
    return results

@mcp.tool(name="unify_entities", description="Merge multiple source entities into a single target entity to resolve duplicates or synonyms.")
@format_output
async def unify_entities(
    ctx: Context,
    sources: List[str] = Field(description="List of entity names to be merged (will be removed)"),
    target: str = Field(description="Name of the resolving entity (will function as the canonical entity)"),
    strategies: Dict[str, str] = Field(description="Strategy per field (e.g. {'description': 'concatenate'}). Options: keep_first, keep_last, concatenate", default_factory=dict)
) -> Any:
    api = await get_api(ctx)
    return await api.merge_entities(sources, target, strategies)
