# Post-Quantum Building Blocks

<p align="center">
  <b>Research-backed, self-verified building blocks for the post-quantum transition and quantum-inspired optimization.</b>
</p>

---

## 🧭 Why PQBlocks

A cryptographically relevant quantum computer would break RSA, Diffie–Hellman, and elliptic-curve cryptography: the algorithms behind almost every TLS session, signature, and encrypted archive today. Data captured now can be decrypted later (*harvest now, decrypt later*).

NIST has standardised the replacements:
- **ML-KEM** (FIPS 203) — Module-Lattice-Based Key-Encapsulation Mechanism
- **ML-DSA** (FIPS 204) — Module-Lattice-Based Digital Signature Algorithm
- **SLH-DSA** (FIPS 205) — Stateless Hash-Based Digital Signature Algorithm

Swapping algorithms is the easy part. A real migration also needs:

| The transition needs… | Because… |
|---|---|
| **Inventory** | You cannot migrate cryptography you have not found. |
| **Correct implementations** | A wrong ML-KEM is worse than none. Conformance must be proven against official vectors. |
| **Interoperable formats** | Larger keys, ciphertexts, and signatures must travel through real protocols and file formats. |
| **Hybrid modes** | Pairing post-quantum with proven classical algorithms keeps security if either one fails. |
| **Verification** | "We upgraded a library" is not proof that every path moved. |

**PQBlocks builds those pieces.** Each one is a small, independently installable package (for pip or npm) that does one job well, is tested against official vectors where they exist, and tells you plainly what it does **not** do.

---

## 🧩 The Five Pillars

=== "🔐 PQ Cryptography"
    ML-KEM, ML-DSA, and SLH-DSA through maintained implementations; hybrid key exchange and signatures; safe defaults for files, tokens, and messages.

    - **pqblocks-core**: Unified hybrid KEM and signature SDK
    - **pqblocks-primitives**: FIPS 203/204/205 bindings and primitives

=== "🧾 Migration & Readiness"
    Find cryptography in code and on the wire, produce CycloneDX CBOMs, score readiness, enforce policy-as-code in CI, and assemble compliance evidence.

    - **pqblocks-scan**: Static analysis crypto inventory scanner
    - **pqblocks-cbom**: CycloneDX 1.5 CBOM enricher and readiness scorer
    - **pqblocks-policy**: Policy-as-code gate enforcing CNSA 2.0
    - **pqblocks-cnsa-evidence**: NSA CNSA 2.0 compliance evidence dossier
    - **pqblocks-lint**: AST-based static linter for deprecated crypto

=== "📡 Interoperability"
    Wire formats, JOSE / JWE, X.509 and CSR, and TLS hybrid groups: carrying larger post-quantum keys, ciphertexts, and signatures through real protocols.

    - **pqblocks-jwe**: Compact 5-part hybrid JWE tokens (ML-KEM-768 + X25519)
    - **pqblocks-jose**: Hybrid JWS signing with ML-DSA-65 / Ed25519
    - **pqblocks-tls-interop**: TLS 1.3 hybrid key exchange validators
    - **pqblocks-csr-pop**: ML-KEM PKCS#10 Certificate Signing Request POP engine
    - **pqblocks-wire**: Length-prefixed binary container format

=== "🔬 Conformance"
    Run official NIST ACVP and Wycheproof vectors, cross-check implementations, and prove a migration actually landed.

    - **pqblocks-acvp**: Automated NIST ACVP test vector runner
    - **pqblocks-fips-check**: Strict FIPS 203/204 wire buffer validator

=== "🌀 Quantum-Inspired Optimization"
    Classical heuristic solvers modelled on quantum dynamics, such as Simulated Bifurcation, QUBO, and annealing. Kept strictly separate from security: **no cryptographic claims**.

    - **pqblocks-bifurcation**: Ballistic and discrete Simulated Bifurcation (bSB/dSB)
    - **pqblocks-qubo**: Unified mathematical representations for QUBO and Ising models
    - **pqblocks-qubo-bench**: Benchmarking harness for combinatorial solvers
    - **pqblocks-anneal-sa**: Simulated Annealing heuristic solver
    - **pqblocks-anneal-sqa**: Simulated Quantum Annealing algorithm
    - **pqblocks-digital-anneal**: Digital Annealing heuristic solver

---

## ⚡ 30-Second Quickstart: Hybrid JWE

```python
# pip install pqblocks-jwe
from pqblocks_jwe import encrypt_jwe, decrypt_jwe, generate_hybrid_keypair

# 1. Generate post-quantum hybrid keypair (ML-KEM-768 + X25519)
priv, pub = generate_hybrid_keypair()

# 2. Encrypt token
payload = b'{"sub":"service-agent-42","scope":"read:pqc"}'
token = encrypt_jwe(payload, pub)

# 3. Decrypt token
decrypted = decrypt_jwe(token, priv)
assert decrypted == payload
print("Decrypted payload:", decrypted.decode("utf-8"))
```

---

## 🛡️ Trust & Verification Principles

1. **Every claim cites its source:** Every benchmark number cites the command, commit SHA, and test environment.
2. **Losing cases are published:** We report where our implementations lose or where trade-offs exist.
3. **Self-verified, never certified:** We state plainly: code is tested against NIST ACVP vectors, but no package claims government CMVP / FIPS 140-3 validation.
4. **Clean-room proven:** Every package is proven in an isolated clean-room virtual environment across Python 3.10–3.14 (and Node.js for npm).

*Part of PQBlocks — a QubitRock project. Licensed under Apache-2.0.*
