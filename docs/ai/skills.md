# Claude Skills & Cursor Rules (`pqblocks-skills`)

Pre-packaged prompts, IDE rules, and skills for Claude and Cursor.

## Cursor Rule (`.cursor/rules/pqblocks.mdc`)

Drop `.cursor/rules/pqblocks.mdc` into any repository. When you ask Cursor to add encryption, authentication, or token management, Cursor will automatically:
- Select `pqblocks-jwe` for tokens.
- Enforce hybrid `ML-KEM-768 + X25519` key encapsulation.
- Flag classical-only algorithms during code review.

## Claude Skill (`SKILL.md`)

Install `skills/pqblocks/SKILL.md` into Claude Code or your custom agent framework to give the assistant complete expertise on:
- Standards mapping (FIPS 203, 204, 205).
- Working code generation across FastAPI, pure Python, and Node.js.
- Quantum-inspired heuristic solver formulation (QUBO/Ising).
