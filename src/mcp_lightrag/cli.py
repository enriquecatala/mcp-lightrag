"""
Command-line interface for the LightRAG MCP server.
"""

import argparse
import logging
import sys
import os

from .mcp_tools import mcp

def setup_logging(level: str = "INFO"):
    """Configure structured logging for the server."""
    logging.basicConfig(
        level=getattr(logging, level),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stderr)]
    )

def main():
    """Entry point for starting the MCP server."""
    parser = argparse.ArgumentParser(description="LightRAG MCP Server - Bridge between MCP and LightRAG API")
    parser.add_argument("--host", help="LightRAG API host")
    parser.add_argument("--port", type=int, help="LightRAG API port")
    parser.add_argument("--api-key", help="Optional API key for authentication")
    parser.add_argument("--log-level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR"], help="Set logging verbosity")
    
    args = parser.parse_args()
    setup_logging(args.log_level)
    logger = logging.getLogger("mcp_lightrag")
    
    # Override environment variables if CLI args are provided
    if args.host:
        os.environ["LIGHTRAG_HOST"] = args.host
    if args.port:
        os.environ["LIGHTRAG_PORT"] = str(args.port)
    if args.api_key:
        os.environ["LIGHTRAG_API_KEY"] = args.api_key
        
    logger.info("Initializing LightRAG MCP Server...")
    
    try:
        # Run using stdio transport as default for MCP
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Server stopped by user signal")
    except Exception as e:
        logger.exception(f"Critical failure during server execution: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
