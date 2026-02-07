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
from .settings import DEFAULT_SETTINGS
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
    client = LightRAGApiClient(DEFAULT_SETTINGS)
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

@mcp.tool(name="query_knowledge_graph", description="Knowledge-aware search across indexed documents")
@format_output
async def query_knowledge_graph(
    ctx: Context,
    prompt: str = Field(description="The search question or query"),
    search_mode: str = Field(
        description="Search strategy: mix, semantic, keyword, global, hybrid, local, naive",
        default="mix"
    ),
    limit: int = Field(description="Max items to retrieve", default=60),
    context_only: bool = Field(description="Set true to get raw data only", default=False),
    prompt_only: bool = Field(description="Set true to see the generated LLM prompt", default=False),
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

@mcp.tool(name="ingest_text", description="Add raw text directly to the knowledge graph")
@format_output
async def ingest_text(
    ctx: Context,
    content: Union[str, List[str]] = Field(description="Text strings to be indexed")
) -> Any:
    api = await get_api(ctx)
    return await api.add_text(content)

@mcp.tool(name="ingest_file", description="Add a local file's content to the knowledge base")
@format_output
async def ingest_file(
    ctx: Context,
    file_path: str = Field(description="Absolute path to the file")
) -> Any:
    api = await get_api(ctx)
    return await api.index_file(file_path)

@mcp.tool(name="upload_and_index", description="Upload file to server storage and start indexing")
@format_output
async def upload_and_index(
    ctx: Context,
    file_path: str = Field(description="Local path to the file")
) -> Any:
    api = await get_api(ctx)
    return await api.upload_file(file_path)

@mcp.tool(name="ingest_batch", description="Index all files in a directory matching specific criteria")
@format_output
async def ingest_batch(
    ctx: Context,
    directory_path: str = Field(description="Absolute path to the directory"),
    recursive: bool = Field(description="Whether to scan subdirectories", default=False),
    max_depth: int = Field(description="Maximum recursion depth", default=1),
    include_patterns: List[str] = Field(description="Regex patterns for files to include", default_factory=list),
    ignore_patterns: List[str] = Field(description="Regex patterns for files to exclude", default_factory=list)
) -> Any:
    api = await get_api(ctx)
    return await api.ingest_batch(
        directory=directory_path,
        recursive=recursive,
        depth=max_depth,
        include_only=include_patterns,
        ignore_files=ignore_patterns
    )

@mcp.tool(name="list_all_docs", description="Show all documents currently in the system")
@format_output
async def list_all_docs(ctx: Context) -> Any:
    api = await get_api(ctx)
    return await api.get_all_documents()

@mcp.tool(name="check_indexing_status", description="Get status of ongoing document processing")
@format_output
async def check_indexing_status(ctx: Context) -> Any:
    api = await get_api(ctx)
    return await api.get_pipeline_status()

# --- Graph Schema & Health ---

@mcp.tool(name="get_graph_metadata", description="Get node and relationship types from the graph")
@format_output
async def get_graph_metadata(ctx: Context) -> Any:
    api = await get_api(ctx)
    return await api.get_labels()

@mcp.tool(name="verify_server_health", description="Check if LightRAG server is reachable")
@format_output
async def verify_server_health(ctx: Context) -> Any:
    api = await get_api(ctx)
    return await api.check_health()

# --- Entity & Relationship Management ---

@mcp.tool(name="create_entities", description="Manually insert entities into the graph")
@format_output
async def create_entities(
    ctx: Context,
    entities: List[Dict[str, Any]] = Field(description="List of items: {name, type, description, source_id}")
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

@mcp.tool(name="remove_entities", description="Delete specific entities from the graph")
@format_output
async def remove_entities(
    ctx: Context,
    names: List[str] = Field(description="Names of entities to delete")
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

@mcp.tool(name="purge_by_document", description="Delete everything associated with document IDs")
@format_output
async def purge_by_document(
    ctx: Context,
    doc_ids: List[str] = Field(description="IDs of documents to prune from graph")
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

@mcp.tool(name="modify_entities", description="Update details for existing entities")
@format_output
async def modify_entities(
    ctx: Context,
    entities: List[Dict[str, Any]] = Field(description="Updated fields for entities")
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

@mcp.tool(name="connect_entities", description="Define or update relationships between entities")
@format_output
async def connect_entities(
    ctx: Context,
    relations: List[Dict[str, Any]] = Field(description="Relationship definitions: {source, target, description, keywords, type?, weight?, edit_mode?}")
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

@mcp.tool(name="unify_entities", description="Merge multiple entities into one")
@format_output
async def unify_entities(
    ctx: Context,
    sources: List[str] = Field(description="Entities to be merged"),
    target: str = Field(description="Name of the resolving entity"),
    strategies: Dict[str, str] = Field(description="Merge strategy per field: keep_first, keep_last, concatenate", default_factory=dict)
) -> Any:
    api = await get_api(ctx)
    return await api.merge_entities(sources, target, strategies)
