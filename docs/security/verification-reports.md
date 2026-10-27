# Verification Reports & Standards

PQBlocks replaces the outdated marketing term "certified" with transparent, reproducible **Verification Reports**.

## Why We Say "Verified", Never "Certified"

In cryptographic engineering:
- *"Certified"* implies government-accredited laboratory evaluation (e.g., FIPS 140-3 / Cryptographic Module Validation Program - CMVP).
- Using "certified" for open-source self-tested software is an overclaim that misleads security auditors.

Instead, every PQBlocks package ships a `VERIFICATION_REPORT.md` documenting:
1. Exact commit SHA and hardware/OS environment used.
2. Official NIST ACVP known-answer test vectors executed.
3. Edge-case test suites (zero inputs, malformed ASN.1/DER buffers, bit flips).
4. Full mutation testing and branch coverage scores.
5. Exact command to reproduce the verification results independently.

---

## Clean-Room Testing Protocol

Every release package is verified using a clean-room workflow:
1. Built into clean `.whl` and `.tar.gz` sdist artifacts.
2. Installed into a fresh, isolated virtual environment with no access to repository source directories.
3. The installed artifact's test suite and example scripts are executed against Python 3.10, 3.11, 3.12, 3.13, and 3.14 (and Node.js 20/22 for npm modules).
4. Only artifacts that pass cleanly across all runtimes receive the `ready: true` release flag.
