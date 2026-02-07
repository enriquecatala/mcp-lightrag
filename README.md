# LightRAG MCP Server

A Model Context Protocol (MCP) server that enables AI assistants to interact with [LightRAG](https://github.com/HKUDS/LightRAG) knowledge graphs. Query documents, manage entities, and build semantic relationships through a standardized tool interface.
**Optimized for Obsidian Vaults**: The built-in smart upsert and document tracking capabilities make it perfect for agents that need to sync and reason over evolving Obsidian knowledge bases.

## Features

- **Smart Updates**: Intelligent `upsert` logic that detects changes in documents, skipping redundant uploads and re-indexing only when necessary
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

## Setting up as MCP Server

To integrate this server with an MCP client (such as Claude Desktop), add the following configuration to your `mcp-server-config.json` key in your settings file. This configuration uses `uv` to run the server from the source directory.

```json
{
  "mcpServers": {
    "mcp-lightrag": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-lightrag",
        "run",
        "mcp-lightrag",
        "--host",
        "localhost",
        "--port",
        "9621"
      ],
      "env": {
        "LIGHTRAG_API_KEY": "optional_api_key"
      }
    }
  }
}
```

> **Note**: Replace `/absolute/path/to/mcp-lightrag` with the actual full path to where you cloned this repository.

### Smart Document Handling
This server distinguishes itself with an intelligent **Upsert Mechanism** ideal for keeping in sync with **Obsidian Vaults** or other local knowledge bases:
- **New File** → Uploads and indexes immediately.
- **Unchanged File** → Detects identical content and skips (saving time and resources).
- **Modified File** → Automatically removes the old version and indexes the new one.
This allows agents to efficiently "watch" a folder and keep the RAG knowledge graph up-to-date without redundant processing.

## Available Tools

### Search & Query
- `query_knowledge_graph` — Execute specialized RAG queries (mix, semantic, keyword, etc.) to answer questions based on your data.

### Document Management
- `ingest_text` — Index raw text content directly into the graph.
- `ingest_file` — Index a specific local file (absolute path required).
- `upload_and_index` — Upload a file to the server for indexing (handles transfer).
- `ingest_batch` — Recursively scan and index directories with pattern filtering.
- `upsert_document` — Smart document upload: creates new, skips identical, or updates modified documents.
- `find_document` — Search for a document by filename to check status and details.
- `get_latest_documents` — Retrieve a paginated list of recently updated documents.
- `list_all_docs` — List all documents in the system (warning: can be slow for large datasets).
- `check_indexing_status` — Check if the background indexing pipeline is idle or busy.

### Graph Operations
- `create_entities` — Manually insert new entities.
- `modify_entities` — Update attributes of existing entities.
- `remove_entities` — Delete specific entities.
- `unify_entities` — Merge multiple entities into a single canonical entity.
- `connect_entities` — Create or update relationships between entities.
- `purge_by_document` — Delete a document and remove all its associated data from the graph.
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

### Publishing

To publish a new version to PyPI:

1. Update the version in `pyproject.toml`.
2. Build the package:
   ```bash
   uv run python -m build
   ```
3. Upload to PyPI (requires PyPI API token):
   ```bash
   uv run twine upload dist/*
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