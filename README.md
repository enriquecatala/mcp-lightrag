# LightRAG MCP Server

A Model Context Protocol (MCP) server that enables AI assistants to interact with [LightRAG](https://github.com/HKUDS/LightRAG) knowledge graphs. Query documents, manage entities, and build semantic relationships through a standardized tool interface.

## Features

- **Knowledge Graph Queries**: Perform semantic, keyword, or hybrid searches across your indexed documents
- **Document Ingestion**: Add text, files, or entire directories to your knowledge base
- **Entity Management**: Create, update, merge, and delete entities in the graph
- **Relationship Handling**: Define and modify connections between entities
- **Robust Connectivity**: Automatic retry with exponential backoff for reliable API communication
- **Flexible Configuration**: Set options via environment variables or command-line arguments

## Installation

```bash
# Clone the repository
git clone https://github.com/enriquecatala/mcp-lightrag.git
cd mcp-lightrag

# Install dependencies
uv sync
```

## Quick Start

1. **Start your LightRAG server** (must be running before the MCP server)

2. **Launch the MCP server**:
   ```bash
   uv run mcp-lightrag --host localhost --port 9621
   ```

3. **Connect your AI assistant** via the MCP protocol (stdio transport)

## Configuration

| Option        | Environment Variable | Default     | Description       |
| ------------- | -------------------- | ----------- | ----------------- |
| `--host`      | `LIGHTRAG_HOST`      | `localhost` | LightRAG API host |
| `--port`      | `LIGHTRAG_PORT`      | `9621`      | LightRAG API port |
| `--api-key`   | `LIGHTRAG_API_KEY`   | *(none)*    | Optional API key  |
| `--log-level` | —                    | `INFO`      | Logging verbosity |

## Available Tools

### Search & Query
- `query_knowledge_graph` — Execute specialized RAG queries (mix, semantic, keyword, etc.) to answer questions based on your data.

### Document Management
- `ingest_text` — Index raw text content directly into the graph.
- `ingest_file` — Index a specific local file (absolute path required).
- `upload_and_index` — Upload a file to the server for indexing (handles transfer).
- `ingest_batch` — Recursively scan and index directories with pattern filtering.
- `find_document` — Check if a document exists and retrieve detailed status (id, status, timestamps, error_msg).
- `get_latest_documents` — Retrieve a paginated list of recently updated documents.
- `list_all_docs` — List all documents in the system (warning: can be slow for large datasets).
- `check_indexing_status` — Check if the background indexing pipeline is idle or busy.

### Graph Operations
- `create_entities` — Manually insert new entities.
- `modify_entities` — Update attributes of existing entities.
- `remove_entities` — Delete specific entities.
- `unify_entities` — Merge multiple entities into a single canonical entity.
- `connect_entities` — Create or update relationships between entities.
- `purge_by_document` — Remove all data associated with specific documents.
- `get_graph_metadata` — Explore the graph schema (available node labels and relationship types).

### System
- `verify_server_health` — Check if the LightRAG API is reachable and healthy.

## Development

```bash
# Install dev dependencies
uv sync --all-extras

# Run tests
uv run python -m pytest

# Lint code
uv run ruff check src/
```

### Updating the Client

If the LightRAG API evolves, you can regenerate the client using `openapi-python-client`. Ensure your LightRAG server is running (e.g., at `http://localhost:9621`), then run:

```bash
uv tool run openapi-python-client generate \
  --url http://localhost:9621/openapi.json \
  --output-path src/mcp_lightrag/client/light_rag_server_api_client \
  --meta none \
  --overwrite
```

This will update the client code in `src/mcp_lightrag/client/light_rag_server_api_client` based on the latest OpenAPI specification.

## License

MIT