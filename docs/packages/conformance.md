# Conformance Packages

Proving correctness against official NIST vectors, testing edge cases, and validating wire invariants.

---

## pqblocks-acvp
- **Repository:** [`PQBlocks/acvp-conformance`](https://github.com/PQBlocks/acvp-conformance)
- **Standard:** NIST Automated Cryptographic Validation Protocol (ACVP)
- **Install:** `pip install pqblocks-acvp`

Test runner executing official NIST ACVP known-answer test vectors (KAT) for ML-KEM and ML-DSA to prove mathematical and behavioral equivalence.

```python
from pqblocks_acvp import run_acvp_vector_set

results = run_acvp_vector_set("tests/vectors/ML-KEM-keyGen-FIPS203.json")
assert results.failed == 0
print(f"Verified {results.passed}/{results.total} official vectors.")
```

---

## pqblocks-fips-check
- **Repository:** [`PQBlocks/fips-boundary-validator`](https://github.com/PQBlocks/fips-boundary-validator)
- **Standard:** FIPS 203 / 204 Wire Invariants
- **Install:** `pip install pqblocks-fips-check`

Enforces strict boundary checking on incoming byte buffers. Rejects truncated, malformed, or out-of-spec key material before reaching cryptographic engines.
