# Migration & Readiness Packages

Tooling to discover cryptographic usage across repositories, generate Cryptography Bills of Materials (CBOM), score quantum readiness, and enforce policy-as-code gates in CI/CD.

---

## pqblocks-scan
- **Repository:** [`PQBlocks/cbom-scanner`](https://github.com/PQBlocks/cbom-scanner)
- **Standard:** CycloneDX 1.5 CBOM, NIST SP 800-131A
- **Install:** `pip install pqblocks-scan`

Static analysis scanner inspecting Python, JavaScript, and binary configurations to locate classical and post-quantum cryptographic primitives.

```bash
# Scan source tree and emit CycloneDX CBOM
pqblocks-scan --dir ./src --format cyclonedx --output cbom.json
```

---

## pqblocks-cbom
- **Repository:** [`PQBlocks/cbom-enricher`](https://github.com/PQBlocks/cbom-enricher)
- **Standard:** CycloneDX 1.5 CBOM Specification, NIST IR 8547
- **Install:** `pip install pqblocks-cbom`

Enriches raw CBOM files with quantum vulnerability scores, transition deadlines (CNSA 2.0 / ANSSI / BSI), and algorithm deprecation flags.

```python
from pqblocks_cbom import enrich_cbom, score_readiness

cbom = enrich_cbom("cbom.json")
score = score_readiness(cbom)
print(f"Readiness Score: {score.percentage}% (CNSA 2.0 Compliant: {score.cnsa_compliant})")
```

---

## pqblocks-policy
- **Repository:** [`PQBlocks/crypto-policy-engine`](https://github.com/PQBlocks/crypto-policy-engine)
- **Standard:** NSA CNSA 2.0, ANSSI Guidelines, BSI TR-02102
- **Install:** `pip install pqblocks-policy`

Policy-as-code engine designed to run in continuous integration gates. Fails builds that introduce deprecated classical algorithms or unapproved parameters.

---

## pqblocks-cnsa-evidence
- **Repository:** [`PQBlocks/cnsa-evidence-pack`](https://github.com/PQBlocks/cnsa-evidence-pack)
- **Standard:** NSA CNSA 2.0 Mandate
- **Install:** `pip install pqblocks-cnsa-evidence`

Assembles an audit-ready compliance dossier mapping all deployed algorithms against the NSA CNSA 2.0 timeline and requirements.

---

## pqblocks-lint
- **Repository:** [`PQBlocks/pqc-lint`](https://github.com/PQBlocks/pqc-lint)
- **Standard:** Python AST Analysis
- **Install:** `pip install pqblocks-lint`

Lightweight AST linter that catches insecure calls to legacy cryptography libraries (`hashlib.md5`, `pyca/cryptography` RSA/DSA key generation) directly in pre-commit hooks.
