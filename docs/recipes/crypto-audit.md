---
title: How to check if my app still uses RSA or ECC
description: Find quantum-vulnerable RSA and elliptic-curve cryptography in source code, grade post-quantum readiness and emit a CycloneDX 1.6 CBOM with pqblocks-scan.
---

# How to check if my app still uses RSA or ECC

<p class="pqb-lead">Inventory the cryptography in your code, mark what a quantum computer would break, score readiness and produce a CycloneDX 1.6 CBOM, the starting point of every migration. Uses <code>pqblocks-scan</code>.</p>

## The problem

You cannot migrate cryptography you have not found. RSA and ECC hide in key generation, TLS settings, JWT libraries and vendored code. Regulators and customers increasingly ask for a Cryptography Bill of Materials (CBOM), and NIST IR 8547 and CNSA 2.0 put dates on retiring these algorithms.

## Install

```bash
pip install git+https://github.com/PQBlocks/cbom-scanner
```

## Complete working code

```python title="crypto_audit.py"
--8<-- "recipes/code/crypto_audit.py"
```

Output:

```text
app.py:3   RSA-2048     QUANTUM-VULNERABLE
app.py:4   ECDSA-P256   QUANTUM-VULNERABLE
app.py:6   SHA-256      ok
readiness: 47.17 D | CBOM spec 1.6
```

## How it works

1. `Discovery` parses Python by syntax tree (other languages by pattern) and records each algorithm with its line number.
2. Each finding is classified: RSA and ECDSA are quantum-vulnerable (Shor); SHA-256 is not.
3. `CARSScorer` turns the findings into a readiness score and an A–F grade, following the CARS model.
4. `CBOMGenerator` writes a CycloneDX 1.6 CBOM you can store with your SBOM or hand to auditors.

## Scan a whole repository

The package also ships a command-line scanner that writes CBOM and SARIF for a directory and can gate CI on the grade. See its [README](https://github.com/PQBlocks/cbom-scanner#readme) and the [`examples/ci_gate.py`](https://github.com/PQBlocks/cbom-scanner/blob/main/examples/ci_gate.py) script.

## Things to know

- Static scanning finds algorithms named in code. Algorithms chosen at runtime or hidden behind library defaults need a TLS probe ([`pqblocks-tls-interop`](../packages/tls-interop.md)) or data-flow analysis ([`pqblocks-lint`](../packages/lint.md)).
- Alpha status: files the scanner cannot parse are reported as scan errors, never silently skipped.

## Next steps

- [`pqblocks-cbom`](../packages/cbom.md): enrich the CBOM with quantum-safety and CNSA 2.0 classifications
- [`pqblocks-policy`](../packages/policy.md): fail CI when a forbidden algorithm appears
- [`pqblocks-cnsa-evidence`](../packages/cnsa-evidence.md): build a compliance evidence pack
