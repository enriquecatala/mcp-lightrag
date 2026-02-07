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
- `query_knowledge_graph` — Semantic search across indexed documents

### Document Management
- `ingest_text` — Add raw text to the knowledge base
- `ingest_file` — Index a local file
- `ingest_batch` — Bulk index files from a directory
- `upload_and_index` — Upload and process a file
- `list_all_docs` — List indexed documents
- `check_indexing_status` — View pipeline processing status

### Graph Operations
- `create_entities` — Add new entities
- `modify_entities` — Update existing entities
- `remove_entities` — Delete entities
- `unify_entities` — Merge multiple entities into one
- `connect_entities` — Create or update relationships
- `purge_by_document` — Remove all data from specific documents
- `get_graph_metadata` — Retrieve node and relationship types

### System
- `verify_server_health` — Check LightRAG API availability

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