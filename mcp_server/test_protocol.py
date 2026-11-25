"""Protocol smoke test using the official SDK client and a fresh subprocess."""
import asyncio
import os
from pathlib import Path
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    params = StdioServerParameters(
        command=sys.executable,
        args=[str(Path(__file__).resolve().with_name("catalog_server.py"))],
        env={k: os.environ[k] for k in ("PATH", "LANG", "SYSTEMROOT") if k in os.environ},
    )
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            assert {t.name for t in tools} == {
                "list_challenges", "get_challenge", "get_research_status"}
            assert all(t.annotations and t.annotations.readOnlyHint for t in tools)
            result = await session.call_tool("get_challenge", {"challenge_id": "inference-002"})
            assert not result.isError and "4069" in str(result)
            result = await session.call_tool("get_challenge", {"challenge_id": "../../private"})
            assert not result.isError and "Unknown public challenge ID" in str(result)
            result = await session.call_tool("list_challenges", {"track": "training"})
            assert not result.isError and "training-001" in str(result)
            assert "inference-002" not in str(result)
            result = await session.call_tool("get_research_status", {})
            assert not result.isError and "bootstrap" in str(result)
    print("Read-only MCP stdio protocol smoke test passed.")

if __name__ == "__main__":
    asyncio.run(main())
