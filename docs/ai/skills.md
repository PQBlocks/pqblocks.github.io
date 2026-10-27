---
title: PQBlocks Claude skill, Cursor rule and AGENTS.md
description: Drop-in guidance that makes Claude Code, Cursor and other coding agents use the PQBlocks post-quantum packages correctly - generated from executed package quickstarts.
---

# Claude skill, Cursor rule and AGENTS.md

<p class="pqb-lead">The <a href="https://github.com/PQBlocks/pqblocks-skills"><code>pqblocks-skills</code></a> repository gives coding agents PQBlocks guidance without running a server. All three files are generated from the same executed catalog as this site.</p>

## What the guidance tells an agent

1. Use the documented API only, from the package reference; never guess function names.
2. Never hand-roll post-quantum cryptography.
3. Hybrid by default: ML-KEM-768 + X25519 and ML-DSA-65 + Ed25519.
4. Never pass a `seed` to production key generation.
5. Never log or return secret keys or shared secrets.
6. Say exactly what is true: implements FIPS 203/204/205, not FIPS 140-3 / CMVP validated, not audited, pre-1.0.
7. Quantum-inspired packages are optimisation, never security.
8. Use the exact install line listed for each package.

Then a task-to-package table maps over twenty common tasks to the right package, install line and import.

## Claude skill

The skill is `skills/pqblocks/` with a short `SKILL.md` and one reference file per package (install, import, command line, executed quickstart, evidence links). Claude loads a reference file only when it needs that package.

=== "Claude Code (personal)"

    ```bash
    git clone https://github.com/PQBlocks/pqblocks-skills
    mkdir -p ~/.claude/skills && cp -r pqblocks-skills/skills/pqblocks ~/.claude/skills/
    ```

=== "Claude Code (one project)"

    ```bash
    git clone https://github.com/PQBlocks/pqblocks-skills
    mkdir -p .claude/skills && cp -r pqblocks-skills/skills/pqblocks .claude/skills/
    ```

## Cursor rule

```bash
mkdir -p .cursor/rules
curl -fsSL https://raw.githubusercontent.com/PQBlocks/pqblocks-skills/main/.cursor/rules/pqblocks.mdc \
  -o .cursor/rules/pqblocks.mdc
```

The rule applies when Cursor works on code that touches RSA, ECDSA, ECDH, X25519, JWT signing, key exchange, file encryption, CBOMs, CNSA 2.0, ML-KEM, ML-DSA, SLH-DSA, QUBO or Ising.

## AGENTS.md template

For Copilot, Codex, Gemini, Aider and any agent that reads `AGENTS.md`:

```bash
curl -fsSL https://raw.githubusercontent.com/PQBlocks/pqblocks-skills/main/AGENTS.md -o AGENTS.md
```

If your project already has an `AGENTS.md`, append the PQBlocks sections to it.

## Keeping it current

The files are regenerated whenever the package catalog changes (`python3 scripts/gen_skills.py`), so they follow API changes in the packages instead of drifting from them.
