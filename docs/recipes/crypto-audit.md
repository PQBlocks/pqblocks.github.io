# How to Scan a Codebase for Classical Cryptography

Learn how to scan an application repository for legacy classical algorithms (RSA, DH, DSA, classical curves), generate a CycloneDX 1.5 CBOM, and score quantum readiness.

## The Problem

Organizations cannot upgrade what they cannot find. Hard-coded RSA keys, legacy JWT setups, and classical TLS ciphers linger undetected in application repositories.

## Installation

```bash
pip install pqblocks-scan pqblocks-cbom
```

## Step 1: Scan Source Code

Run `pqblocks-scan` pointing to your project directory:

```bash
pqblocks-scan --dir ./src --format cyclonedx --output cbom.json
```

Output preview:
```
[HIGH] src/auth/token.py:14 -> RSA-2048 detected (Vulnerable to Shor's algorithm)
[MEDIUM] src/net/client.py:42 -> SECP256R1 classical curve detected
[INFO] Generated CycloneDX 1.5 CBOM -> cbom.json (18 components found)
```

## Step 2: Enrich CBOM & Score Readiness

```python
from pqblocks_cbom import enrich_cbom, score_readiness

# Load and enrich CBOM with NIST and CNSA 2.0 timelines
cbom = enrich_cbom("cbom.json")
score = score_readiness(cbom)

print(f"Overall Quantum Readiness Score: {score.percentage}%")
print(f"Classical Vulnerabilities: {score.classical_count}")
print(f"Post-Quantum Hybrid Components: {score.hybrid_count}")
print(f"Meets CNSA 2.0 2030 Mandate: {score.cnsa_compliant}")
```

## Step 3: Enforce Policy Gate in CI/CD

Integrate into GitHub Actions:

```yaml
name: Crypto Policy Gate
on: [pull_request]

jobs:
  pqc-audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install pqblocks-scan pqblocks-policy
      - run: pqblocks-scan --dir ./src --output cbom.json
      - run: python -c "from pqblocks_policy import PolicyEngine, PolicyPreset; assert PolicyEngine(PolicyPreset.CNSA_2_0).check('cbom.json').is_clean"
```
