# The Post-Quantum Transition Mapped

The migration away from RSA and ECC is a multi-year engineering program. PQBlocks provides tools for every phase of the transition.

```mermaid
flowchart TD
    subgraph Phase 1: Discover
        A["Audit Repositories"] -->|pqblocks-scan| B["Generate CBOM (CycloneDX 1.5)"]
        B -->|pqblocks-cbom| C["Score Quantum Readiness"]
    end

    subgraph Phase 2: Govern
        C -->|pqblocks-policy| D["CI/CD Policy Gates (CNSA 2.0)"]
        D -->|pqblocks-cnsa-evidence| E["Auditor Evidence Dossier"]
    end

    subgraph Phase 3: Migrate
        E -->|pqblocks-core| F["Hybrid KEM & Signatures"]
        F -->|pqblocks-jwe / pqblocks-jose| G["Post-Quantum Tokens (JWE / JWS)"]
        F -->|pqblocks-tls-interop| H["TLS 1.3 Hybrid Handshakes"]
        F -->|pqblocks-csr-pop| I["X.509 PKCS#10 Proof of Possession"]
    end

    subgraph Phase 4: Verify
        G & H & I -->|pqblocks-acvp| J["NIST ACVP Vector Validation"]
        J -->|pqblocks-fips-check| K["Wire Boundary Invariant Proof"]
    end
```

## Transition Timeline & Regulatory Milestones

| Year | Standard / Mandate | What Changes | Relevant PQBlocks Tool |
|---|---|---|---|
| **2024** | NIST FIPS 203, 204, 205 | Initial PQC standards finalized | `pqblocks-core`, `pqblocks-acvp` |
| **2026** | NSA CNSA 2.0 (Phase 1) | Software & firmware signing begins PQC migration | `pqblocks-policy`, `pqblocks-cnsa-evidence` |
| **2030** | NIST SP 800-131A Rev 3 | RSA-2048 and classical ECC deprecated | `pqblocks-scan`, `pqblocks-lint` |
| **2033** | NSA CNSA 2.0 (Phase 2) | Exclusively quantum-safe cryptography mandatory | `pqblocks-cbom`, `pqblocks-jwe` |
