# Portable read-only MCP catalog

This Node.js MCPB packages the public, dated SiliconArena challenge catalog. It exposes exactly three read-only tools. It has no network calls, shell execution, arbitrary file access, credentials, tracking, or enrollment. The only project data it reads is the bundled challenges.json. It does not execute RTL, request compute, publish anything, or automatically install itself.

Source is MIT. The bundle includes the official MCP TypeScript SDK (maintenance v1 line) and dependencies with their own licenses. The release build records dependency versions in package-lock.json, runs a real stdio protocol test, and uses an isolated hosted CI runner. Clients should verify the published SHA-256 and review before installation. Catalog is a snapshot, not live scores; its public links lead to current project evidence.

MCP Registry name: `io.github.rtl-ai/siliconarena-catalog`. A registry listing is not an endorsement, an agent count, or a hosted MCP endpoint.
