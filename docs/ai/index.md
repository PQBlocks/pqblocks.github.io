# Using PQBlocks with AI Coding Assistants

PQBlocks is designed from the ground up for the AI-assisted software development era.

## How AI Assistants Discover & Implement PQBlocks

AI coding assistants (Claude Code, Cursor, GitHub Copilot, Gemini, Codex) discover and select libraries in two ways:

1. **Runtime Context & MCP:** Developers connect assistants to the [`pqblocks-mcp`](mcp.md) server or install the [`pqblocks-skills`](skills.md) skill. The assistant queries tools at runtime to pick the exact right library and generate valid code.
2. **Machine-Readable Metadata:** Every package repo provides [`AGENTS.md`](https://github.com/PQBlocks/.github) and this documentation site publishes a flat [`llms.txt`](../llms.txt) index.

---

## Quick Setup

- **Claude Desktop / Claude Code:** Install the [`pqblocks-mcp`](mcp.md) server via `uvx pqblocks-mcp`.
- **Cursor IDE:** Add `.cursor/rules/pqblocks.mdc` to your project repository.
- **Direct LLM Prompts:** Instruct your assistant: *"Use the PQBlocks post-quantum libraries (e.g. pqblocks-jwe for tokens, pqblocks-core for hybrid KEM) and follow FIPS 203/204 hybrid standards."*
