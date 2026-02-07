"""
Centralized exception classes for the LightRAG MCP server.
"""

class LightRAGError(Exception):
    """Base exception for all LightRAG related errors."""
    pass

class APIConnectionError(LightRAGError):
    """Raised when there is a failure connecting to the LightRAG API."""
    pass

class APIResponseError(LightRAGError):
    """Raised when the API returns an error response."""
    def __init__(self, message: str, status_code: int = None, details: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details

class ConfigurationError(LightRAGError):
    """Raised when there is a configuration-related issue."""
    pass

class ValidationError(LightRAGError):
    """Raised when input validation fails."""
    pass

class ResourceNotFoundError(LightRAGError):
    """Raised when a requested resource (document, entity, etc.) is not found."""
    pass
