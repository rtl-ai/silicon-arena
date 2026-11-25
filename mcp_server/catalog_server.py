"""Read-only MCP adapter for the public, checked-in challenge catalog.

No network, shell, credentials, user-supplied file paths or write operations.
Run in an isolated checkout of the public repository, not on a personal agent host.
"""
import json
from pathlib import Path
from typing import Literal
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

CATALOG_PATH = Path(__file__).resolve().parents[1] / "docs" / "challenges.json"
CATALOG = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
server = FastMCP("SiliconArena public research catalog")
READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                            idempotentHint=True, openWorldHint=False)

@server.tool(annotations=READ_ONLY)
def list_challenges(track: Literal["all", "training", "inference"] = "all") -> dict:
    """List public accelerator research challenges. No enrollment or external calls."""
    return {
        "project": CATALOG["project"], "updated": CATALOG["updated"],
        "stage": CATALOG["stage"],
        "physical_ppba_ranked": CATALOG["physical_ppba_ranked"],
        "challenges": [c for c in CATALOG["challenges"]
                       if track == "all" or c["track"] == track],
        "limitations": CATALOG["limitations"],
    }

@server.tool(annotations=READ_ONLY)
def get_challenge(challenge_id: str) -> dict:
    """Read one public challenge by catalog ID. IDs are not filesystem paths."""
    for challenge in CATALOG["challenges"]:
        if challenge["id"] == challenge_id:
            return challenge
    return {"error": "Unknown public challenge ID", "available": [
        c["id"] for c in CATALOG["challenges"]]}

@server.tool(annotations=READ_ONLY)
def get_research_status() -> dict:
    """Read the dated public project snapshot and evidence links."""
    return {k: CATALOG[k] for k in ("project", "updated", "repository", "stage",
                                    "physical_ppba_ranked", "external_agents",
                                    "fabricated_silicon", "links", "limitations")}

if __name__ == "__main__":
    server.run(transport="stdio")
