# Package Catalog Overview

PQBlocks currently maintains 26 specialized packages across 5 domains. Every package ships its source code, tests, official NIST vector verifications, benchmark evidence, and security notes.

## Summary Directory

| Package | Domain | Primary Standard | Install Command |
|---|---|---|---|
| **[pqblocks-core](crypto.md#pqblocks-core)** | PQ Cryptography | FIPS 203 / FIPS 204 | `pip install pqblocks-core` |
| **[pqblocks-primitives](crypto.md#pqblocks-primitives)** | PQ Cryptography | FIPS 203/204/205 | `pip install pqblocks-primitives` |
| **[pqblocks-jwe](interop.md#pqblocks-jwe)** | Interoperability | RFC 7516 + FIPS 203 | `pip install pqblocks-jwe` |
| **[pqblocks-jose](interop.md#pqblocks-jose)** | Interoperability | RFC 7515 + FIPS 204 | `pip install pqblocks-jose` |
| **[pqblocks-tls-interop](interop.md#pqblocks-tls-interop)** | Interoperability | RFC 8446 + X25519MLKEM768 | `pip install pqblocks-tls-interop` |
| **[pqblocks-csr-pop](interop.md#pqblocks-csr-pop)** | Interoperability | PKCS#10 + CMP | `pip install pqblocks-csr-pop` |
| **[pqblocks-wire](interop.md#pqblocks-wire)** | Interoperability | Binary Framing | `pip install pqblocks-wire` |
| **[pqblocks-scan](migration.md#pqblocks-scan)** | Migration | CycloneDX 1.5 CBOM | `pip install pqblocks-scan` |
| **[pqblocks-cbom](migration.md#pqblocks-cbom)** | Migration | NIST IR 8547 | `pip install pqblocks-cbom` |
| **[pqblocks-policy](migration.md#pqblocks-policy)** | Migration | CNSA 2.0 | `pip install pqblocks-policy` |
| **[pqblocks-cnsa-evidence](migration.md#pqblocks-cnsa-evidence)** | Migration | NSA Mandate | `pip install pqblocks-cnsa-evidence` |
| **[pqblocks-lint](migration.md#pqblocks-lint)** | Migration | Python AST | `pip install pqblocks-lint` |
| **[pqblocks-acvp](conformance.md#pqblocks-acvp)** | Conformance | NIST ACVP | `pip install pqblocks-acvp` |
| **[pqblocks-fips-check](conformance.md#pqblocks-fips-check)** | Conformance | FIPS 203/204 Buffer Invariants | `pip install pqblocks-fips-check` |
| **[pqblocks-bifurcation](optimization.md#pqblocks-bifurcation)** | Quantum-Inspired | Goto et al. (bSB/dSB) | `pip install pqblocks-bifurcation` |
| **[pqblocks-qubo](optimization.md#pqblocks-qubo)** | Quantum-Inspired | Ising Hamiltonian | `pip install pqblocks-qubo` |
