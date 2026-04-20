# mcp-lightrag

MCP (Model Context Protocol) server for [LightRAG](https://github.com/HKUDS/LightRAG) — a graph-based Retrieval-Augmented Generation framework.

This fork adds API key header authentication support and fixes compatibility with **LightRAG >= 1.4.13**.

> Original project: [enriquecatala/mcp-lightrag](https://github.com/enriquecatala/mcp-lightrag)

---

## Compatibility

| mcp-lightrag | LightRAG server |
|---|---|
| this fork (`main`) | >= 1.4.13 |
| upstream 0.2.2 | <= 1.4.12 |

---

## What was changed in this fork

### Fix: compatibility with LightRAG >= 1.4.13

LightRAG 1.4.13 removed and renamed several `QueryRequest` parameters.

**Removed parameters (cause `TypeError` on upstream 0.2.2):**

| Old parameter | Status |
|---|---|
| `max_token_for_text_unit` | removed |
| `history_turns` | removed |

**Renamed parameters:**

| Old name | New name |
|---|---|
| `max_token_for_global_context` | `max_relation_tokens` |
| `max_token_for_local_context` | `max_entity_tokens` |

**Removed query mode:**

| Old mode | Status |
|---|---|
| `semantic` | does not exist in `QueryRequestMode` |

Valid query modes: `mix`, `local`, `global`, `hybrid`, `naive`, `bypass`.

### Fix: API key sent as `X-API-Key` header

The original code sent the API key as a `Bearer` token. LightRAG server expects it in the `X-API-Key` header. The `AuthenticatedClient` is now configured with `auth_header_name="X-API-Key"` and `prefix=""`.

### Fix: HTTPS auto-detection for port 443

The original code always built `base_url` as `http://host:port`, causing
HTTP 400 errors when connecting to HTTPS servers (e.g. via nginx on port 443).

**Fixed behavior:**
- Port 443 automatically uses `https://`
- Explicit scheme in `--host` is respected (e.g. `--host https://example.com`)

| Configuration | Result |
|---|---|
| `--host localhost --port 9621` | `http://localhost:9621` |
| `--host example.com --port 443` | `https://example.com:443` |
| `--host https://example.com --port 443` | `https://example.com` |

---

## Installation

### Prerequisites

- Python >= 3.10
- [uv](https://github.com/astral-sh/uv)
- A running LightRAG server >= 1.4.13

### Clone and install

```bash
git clone https://github.com/leskei217/mcp-lightrag.git
cd mcp-lightrag
uv sync
```

---

## Configuration

### Claude Desktop (`claude_desktop_config.json`) (for Windows)

```json
{
  "mcpServers": {
    "mcp-lightrag": {
      "command": "uv",
      "args": [
        "--directory", "C:\\path\\to\\mcp-lightrag",
        "run", "mcp-lightrag",
        "--host", "YOUR_LIGHTRAG_HOST",
        "--port", "9621" 
      ],
      "env": {
        "LIGHTRAG_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

If your LightRAG server has no authentication, omit `LIGHTRAG_API_KEY` entirely.

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `LIGHTRAG_HOST` | `localhost` | LightRAG server host |
| `LIGHTRAG_PORT` | `9621` | LightRAG server port |
| `LIGHTRAG_API_KEY` | *(empty)* | API key (omit if auth disabled) |

---

## Available MCP tools

### Query

| Tool | Description |
|---|---|
| `query_knowledge_graph` | Search the knowledge graph. Modes: `mix`, `local`, `global`, `hybrid`, `naive`, `bypass` |

### Documents

| Tool | Description |
|---|---|
| `ingest_text` | Index raw text directly |
| `ingest_file` | Index a local file |
| `upload_and_index` | Upload a file to server and index it |
| `upsert_document` | Smart upload: create / skip if identical / update if changed |
| `ingest_batch` | Index all files in a directory |
| `list_all_docs` | List all documents (slow on large collections) |
| `find_document` | Find a document by filename |
| `get_latest_documents` | Paginated list of recently updated documents |
| `check_indexing_status` | Check pipeline status (idle/busy) |

### Graph

| Tool | Description |
|---|---|
| `get_graph_metadata` | List node labels and relation types |
| `verify_server_health` | Health check |
| `create_entities` | Add entities manually |
| `remove_entities` | Delete entities by name |
| `modify_entities` | Update entity properties |
| `connect_entities` | Create or update relationships |
| `unify_entities` | Merge duplicate entities |
| `purge_by_document` | Remove all graph data for given document IDs |

---

## Query modes reference

| Mode | Description |
|---|---|
| `mix` | **Recommended.** Combines knowledge graph retrieval with vector search |
| `local` | Entity-focused: returns entities and their direct relationships |
| `global` | Pattern analysis across the full knowledge graph |
| `hybrid` | Combines local and global strategies |
| `naive` | Vector similarity search only, no knowledge graph |
| `bypass` | Direct LLM call, no retrieval |

---

## License

MIT
