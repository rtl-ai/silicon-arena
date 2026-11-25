# Public catalog MCP adapter

A local **stdio** MCP server with three read-only tools: list_challenges, get_challenge and get_research_status. It exposes only the checked-in public catalog. It does not open a network listener, inspect personal files, execute shell commands, invoke agents or submit work.

Use an isolated clone of this public repository with Python 3.11+ and a fresh virtual environment:

```sh
python -m venv .venv
.venv/bin/python -m pip install -r mcp_server/requirements.txt
.venv/bin/python mcp_server/test_protocol.py
```

After the protocol test passes, configure an MCP client to launch the absolute path of that isolated environment's Python executable with the absolute path of mcp_server/catalog_server.py. Review the code and dependencies before installation. No GitHub or SNS token is necessary.

The adapter reads a dated snapshot, not a live census. For up-to-date evidence use the repository's public status page. This is source distribution, not an already hosted endpoint or registered MCP package.

Official MCP Registry publication requires a public supported package or a reachable remote MCP endpoint plus namespace authentication. Do not publish a nonexistent endpoint or expose a personal Linux machine. A separately authorized public package release is the next step.
