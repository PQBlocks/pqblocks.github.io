---
title: About PQBlocks
description: PQBlocks is an open-source engineering organisation for the post-quantum era and a QubitRock project. Scope, principles, roadmap and how to contribute.
---

# About PQBlocks

<p class="pqb-lead">PQBlocks is an open-source engineering organisation for the post-quantum (PQ) era. It is a <strong>QubitRock</strong> project.</p>

## What we build

The post-quantum transition touches every system that uses public-key cryptography, and it needs more than new algorithms. PQBlocks builds the full set of engineering components for it, across five areas:

| Area | Scope |
|---|---|
| **PQ cryptography** | NIST-standard primitives (ML-KEM, ML-DSA, SLH-DSA) through maintained implementations, hybrid modes, tokens, files |
| **Migration & readiness** | Crypto inventory, CBOMs, readiness scoring, policy-as-code, compliance evidence |
| **Interoperability** | TLS, JOSE, X.509 / CSR, wire formats for larger keys, ciphertexts and signatures |
| **Conformance** | Official NIST vectors, cross-implementation checks, strict input validation |
| **Quantum-inspired computing** | Classical optimisation algorithms modelled on quantum dynamics, kept apart from security |

## Principles

- **Standards first.** No novel cryptography; only standardised or peer-reviewed algorithms.
- **Evidence over assertion.** Tests, vectors, benchmarks, sources and a verification report in every repository.
- **Honest limits.** We say "verified", never "certified", and we write down what a package does not do.
- **Independent blocks.** Each package installs and versions on its own, so you adopt only what you need.
- **Built for people and agents.** Documentation that humans can read and coding assistants can use without guessing.

## Roadmap

| Now | Next |
|---|---|
| Python packages across five areas, each in its own repository | PyPI releases for every package (in progress) |
| MCP server, Claude skill, Cursor rule, `llms.txt` | npm modules for JavaScript and TypeScript |
| Executed documentation and recipes | Native SDKs and framework adapters (FastAPI, Django, Express) |
| | Hosted readiness services built on the open packages |

## Contribute

- Browse the organisation on [GitHub](https://github.com/PQBlocks) and read the [contributing guide](https://github.com/PQBlocks/.github/blob/main/CONTRIBUTING.md).
- Every contribution follows the [cryptography policy](https://github.com/PQBlocks/.github/blob/main/CRYPTO-POLICY.md).
- Report vulnerabilities privately, as described in [security](security/security-notes.md#reporting-a-vulnerability).

## Licence

All PQBlocks code is released under the Apache License 2.0. Algorithms are implemented from public standards and cite their sources in each package's `EVIDENCE.md`.
