---
title: PQBlocks MCP server for Claude Code and Cursor
description: pqblocks-mcp is a Model Context Protocol server that recommends the right post-quantum package, returns quickstarts executed against the real package, and flags RSA and ECC in code.
---

# PQBlocks MCP server

<p class="pqb-lead"><code>pqblocks-mcp</code> is a Model Context Protocol (MCP) server for coding agents. It answers "which package, how do I install it, what is the exact code" from a catalog in which every quickstart was executed, and it flags quantum-vulnerable algorithms in code you paste.</p>

[![Source](https://img.shields.io/badge/source-pqblocks--mcp-111827?style=flat-square&logo=github)](https://github.com/PQBlocks/pqblocks-mcp)
![Transport](https://img.shields.io/badge/transport-stdio-0e7490?style=flat-square)
![Dependencies](https://img.shields.io/badge/runtime%20deps-none-334155?style=flat-square)
![Licence](https://img.shields.io/badge/licence-Apache--2.0-334155?style=flat-square)

## Install

The server runs from its GitHub repository with [`uv`](https://docs.astral.sh/uv/); nothing else is needed.

=== "Claude Code"

    ```bash
    claude mcp add pqblocks -- uvx --from git+https://github.com/PQBlocks/pqblocks-mcp pqblocks-mcp
    ```

=== "Claude Desktop"

    Add to `claude_desktop_config.json`:

    ```json
    {
      "mcpServers": {
        "pqblocks": {
          "command": "uvx",
          "args": ["--from", "git+https://github.com/PQBlocks/pqblocks-mcp", "pqblocks-mcp"]
        }
      }
    }
    ```

=== "Cursor"

    Add to `.cursor/mcp.json` in your project (or `~/.cursor/mcp.json`):

    ```json
    {
      "mcpServers": {
        "pqblocks": {
          "command": "uvx",
          "args": ["--from", "git+https://github.com/PQBlocks/pqblocks-mcp", "pqblocks-mcp"]
        }
      }
    }
    ```

=== "VS Code"

    Add to `.vscode/mcp.json`:

    ```json
    {
      "servers": {
        "pqblocks": {
          "type": "stdio",
          "command": "uvx",
          "args": ["--from", "git+https://github.com/PQBlocks/pqblocks-mcp", "pqblocks-mcp"]
        }
      }
    }
    ```

=== "pip"

    ```bash
    pip install git+https://github.com/PQBlocks/pqblocks-mcp
    pqblocks-mcp            # speaks MCP over stdio
    ```

The server has no runtime dependencies. With the official MCP SDK installed (`pip install "pqblocks-mcp[sdk] @ git+https://github.com/PQBlocks/pqblocks-mcp"`) it uses the SDK transport; otherwise it uses its built-in stdio JSON-RPC implementation.

## Tools

| Tool | Input | Returns |
|---|---|---|
| `recommend_package` | `task_description`: the task in plain words | The best package, why, install line, import, executed quickstart, docs link and up to two alternatives |
| `get_snippet` | `package` (full or short name), optional `framework` | Install line, import, the executed quickstart, example scripts and the evidence documents |
| `check_config` | `code_or_config`: pasted code or configuration | Line-numbered findings for RSA, ECDSA, ECDH / NIST curves, DH, DSA, lone X25519 / Ed25519, MD5, SHA-1, 3DES, AES-128, with replacements and packages |
| `list_packages` | optional `category` (area name) | Every package with area, version, status and the install line that works today |

## What a call returns

Asking `recommend_package` for *"sign JWTs with ML-DSA"* returns (shortened):

```json
{
  "recommended_package": "pqblocks-jose",
  "why": "Post-quantum hybrid JOSE library supporting ML-KEM and ML-DSA JWE and JWS tokens.",
  "area": "PQ cryptography",
  "install": "pip install git+https://github.com/PQBlocks/hybrid-jose",
  "import": "pqblocks_jose",
  "quickstart": "from pqblocks_jose import Policy, generate_keypair, encode_jws, decode_jws, ...",
  "docs": "https://github.com/PQBlocks/hybrid-jose/blob/main/README.md",
  "alternatives": [{"package": "pqblocks-jwe-audit", "summary": "..."}]
}
```

## Why agents can trust it

- **Facts come from the packages.** The catalog is built from each package's `pyproject.toml`, README and examples, so it cannot describe an API that does not exist.
- **Every quickstart was executed.** The catalog build runs each README quickstart against the package source; the server ships only verified entries, and its test suite fails if one is not verified.
- **Honest negatives.** If a package's README says it does *not* do something (for example, `pqblocks-jwe` does not encrypt), the recommender will not route that task to it.
- **Limits are stated.** `check_config` matches algorithm names line by line. It cannot see algorithms chosen at runtime, and it says so in every response; use [`pqblocks-scan`](../packages/scan.md) for a whole repository.
