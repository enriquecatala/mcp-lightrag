"""
Data models and type definitions for LightRAG MCP server.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

@dataclass(frozen=True)
class ServerSettings:
    """Settings for the LightRAG API connection."""
    host: str = "localhost"
    port: int = 9621
    api_key: str = ""
    
    @property
    def base_url(self) -> str:
        return f"http://{self.host}:{self.port}"

@dataclass
class QueryParams:
    """Parameters for document queries."""
    query: str
    mode: str = "mix"
    top_k: int = 60
    only_need_context: bool = False
    only_need_prompt: bool = False
    response_type: str = "Multiple Paragraphs"
    max_token_for_text_unit: int = 4096
    max_token_for_global_context: int = 4096
    max_token_for_local_context: int = 4096
    hl_keywords: List[str] = field(default_factory=list)
    ll_keywords: List[str] = field(default_factory=list)
    history_turns: int = 10

@dataclass
class OperationResult:
    """Standardized response for API operations."""
    status: str
    response: Optional[Any] = None
    error: Optional[str] = None
    
    @classmethod
    def success(cls, data: Any) -> "OperationResult":
        return cls(status="success", response=data)
    
    @classmethod
    def failure(cls, error_msg: str) -> "OperationResult":
        return cls(status="error", error=error_msg)

@dataclass
class BatchResult:
    """Statistics for batch operations."""
    total: int
    successful: int
    failed: int
    results: List[Dict[str, Any]]
