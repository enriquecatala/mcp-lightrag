"""
LightRAG MCP Server - A Model Context Protocol server for LightRAG.
"""

__version__ = "0.2.0"

from .mcp_tools import mcp
from .api_client import LightRAGApiClient
from .settings import get_settings

__all__ = ["mcp", "LightRAGApiClient", "get_settings"]
