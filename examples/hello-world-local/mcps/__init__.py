"""Runtime Config Demo - MCPs module.

Arxiv MCP is conditionally created based on environment variables.
"""

import os

from glaip_sdk.mcps import MCP
from dotenv import load_dotenv

load_dotenv(override=True)

# Arxiv MCP - requires authentication headers
_api_key = os.getenv("ARXIV_MCP_API_KEY")
_auth_token = os.getenv("ARXIV_MCP_AUTH_TOKEN")

arxiv_mcp: MCP | None = None

if _api_key and _auth_token:
    arxiv_mcp = MCP(
        name="arxiv-mcp-chen",
        transport="http",
        description="Arxiv MCP for searching academic papers",
        config={
            "url": "https://api.bosa.id/arxiv/mcp/",
        },
        authentication={
            "type": "custom-header",
            "headers": {
                "x-api-key": _api_key,
                "Authorization": f"Bearer {_auth_token}",
            },
        },
    )
deepwiki_mcp = MCP(
    name="deepwiki",
    transport="sse",
    description="DeepWiki MCP for accessing public GitHub repository documentation",
    config={
        "url": "https://mcp.deepwiki.com/sse",
    },
)

__all__ = ["arxiv_mcp", "deepwiki_mcp"]
