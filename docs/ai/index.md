---
title: Using PQBlocks with AI coding assistants
description: Make Claude Code, Cursor, Copilot and other coding agents choose the right post-quantum package and write code against its real API - MCP server, Claude skill, Cursor rules and llms.txt.
---

# Using PQBlocks with AI coding assistants

<div class="pqb-figure" data-figure="hub" data-label="A hub with tiles on dashed links: the tile under the pointer rises and its link turns solid."></div>

<p class="pqb-lead">When you ask an assistant to "add post-quantum encryption", it should pick a real package and call its real API. PQBlocks gives agents the facts at runtime, so they stop guessing function names.</p>

## How do coding agents choose a library?

Assistants pick libraries in two ways. The slow path is training data: what appeared most often in code and docs before the model was trained. The fast path is runtime lookup: tools, documentation and files the agent reads while it works. PQBlocks is built for the fast path. Everything below is generated from one catalog, and every code sample in that catalog was executed against the package before it was published, so the agent never has to invent a function name.

<div class="grid cards" markdown>

-   :material-connection:{ .lg .middle } __[MCP server](mcp.md)__

    ---

    `pqblocks-mcp` gives Claude Code, Cursor and any MCP client four tools: recommend a package, get its executed quickstart, check code for quantum-vulnerable algorithms, list the catalog.

-   :material-head-cog-outline:{ .lg .middle } __[Claude skill and Cursor rules](skills.md)__

    ---

    Drop-in guidance with no server: a Claude skill with one reference file per package, a Cursor rule and an `AGENTS.md` template.

-   :material-file-document-multiple-outline:{ .lg .middle } __[llms.txt and llms-full.txt](../llms.txt)__

    ---

    The whole catalog for agents that read the web: [`llms.txt`](../llms.txt) is the index, [`llms-full.txt`](../llms-full.txt) adds every quickstart and recipe.

-   :material-file-code-outline:{ .lg .middle } __AGENTS.md in every repository__

    ---

    Each package repository ships its own `AGENTS.md` with correct imports and pitfalls, so an agent working inside the repo has it too.

</div>

## Which one should I use?

| You use | Set up | What the agent gets |
|---|---|---|
| Claude Code, Claude Desktop, Cursor, Windsurf, any MCP client | [MCP server](mcp.md) | Live tools: recommendation, executed quickstarts, code check |
| Claude Code without a server | [Claude skill](skills.md#claude-skill) | Rules, task-to-package table, per-package reference |
| Cursor without a server | [Cursor rule](skills.md#cursor-rule) | Rules and task table, applied when crypto code is touched |
| Any other agent (Copilot, Codex, Gemini, Aider) | [`AGENTS.md` template](skills.md#agentsmd-template) | Rules and task table in the project root |

## A prompt that works

Without any setup, this prompt points an assistant at the right sources:

```text
Use the PQBlocks post-quantum packages. Read https://pqblocks.github.io/llms-full.txt first and use only
the APIs shown there. Prefer hybrid ML-KEM-768 + X25519 and ML-DSA-65 + Ed25519, never pass a seed to
key generation, and never log secret keys.
```
