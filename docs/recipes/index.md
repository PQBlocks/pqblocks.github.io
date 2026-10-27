---
title: Post-quantum recipes
description: Complete, tested solutions to common post-quantum tasks in Python - sign JWTs with ML-DSA, hybrid X25519 + ML-KEM, encrypt files, find RSA and ECC in code, solve Max-Cut.
---

# Recipes

<p class="pqb-lead">One page per question developers actually ask. Every recipe is a complete program that was executed against the package source before this site was published, and each page shows the output it printed.</p>

<div class="grid cards" markdown>

-   :material-signature-freehand:{ .lg .middle } __[How to sign JWTs with ML-DSA in Python](jwt-ml-dsa.md)__

    ---

    Hybrid ML-DSA-65 + Ed25519 JWS tokens with `pqblocks-jose`, including a wrong-key rejection check.

-   :material-api:{ .lg .middle } __[How to add post-quantum tokens to FastAPI](fastapi-pqc.md)__

    ---

    Issue and verify ML-DSA-signed bearer tokens in a FastAPI service, with a tamper test.

-   :material-key-chain-variant:{ .lg .middle } __[How to do hybrid X25519 + ML-KEM key exchange](hybrid-kem.md)__

    ---

    Establish a shared secret that survives a break of either ML-KEM or X25519, with `pqblocks-primitives`.

-   :material-file-lock-outline:{ .lg .middle } __[How to encrypt files with a post-quantum key](encrypt-files.md)__

    ---

    Passphrase-sealed key files and ML-KEM-768 + X25519 file encryption with `pqblocks-files`.

-   :material-magnify-scan:{ .lg .middle } __[How to check if my app still uses RSA or ECC](crypto-audit.md)__

    ---

    Inventory quantum-vulnerable algorithms, grade readiness and emit a CycloneDX 1.6 CBOM with `pqblocks-scan`.

-   :material-graph-outline:{ .lg .middle } __[How to solve Max-Cut with a quantum-inspired solver](qubo-maxcut.md)__

    ---

    Simulated Bifurcation on an Ising model, checked against brute force, with `pqblocks-bifurcation`.

</div>

!!! tip "How these recipes stay correct"
    The code on each page is included verbatim from [`docs/recipes/code/`](https://github.com/PQBlocks/pqblocks.github.io/tree/main/docs/recipes/code), and `scripts/check_recipes.py` runs every file before a release of the site. If a package API changes, the check fails before the page can go wrong.
