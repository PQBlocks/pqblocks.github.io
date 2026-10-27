# PQBlocks MCP Server (`pqblocks-mcp`)

The Model Context Protocol (MCP) server allows AI assistants to recommend packages, generate tested code snippets, and audit security configurations directly in your editor.

## Tools Provided

| Tool | Purpose | Example Input |
|---|---|---|
| `recommend_package` | Recommends the right PQBlocks package and explains why | `{"task_description": "encrypt JWT post-quantum"}` |
| `get_snippet` | Emits working, tested copy-paste code with install steps | `{"package": "pqblocks-jwe", "framework": "fastapi"}` |
| `check_config` | Flags deprecated classical crypto (RSA, ECDSA) and advises migration | `{"code_or_config": "rsa.generate_key(2048)"}` |
| `list_packages` | Lists all 26 packages by transition domain | `{"category": "Interoperability"}` |

## Client Configuration

### Claude Desktop (`claude_desktop_config.json`)
```json
{
  "mcpServers": {
    "pqblocks": {
      "command": "uvx",
      "args": ["pqblocks-mcp"]
    }
  }
}
```

### Cursor IDE (`.cursor/mcp.json`)
```json
{
  "mcpServers": {
    "pqblocks": {
      "command": "python",
      "args": ["-m", "pqblocks_mcp.server"]
    }
  }
}
```
