---
title: How to sign JWTs with ML-DSA in Python
description: Sign and verify JSON Web Tokens with hybrid ML-DSA-65 + Ed25519 (FIPS 204) in Python using pqblocks-jose. Complete, tested code and output.
---

# How to sign JWTs with ML-DSA in Python

<p class="pqb-lead">Use <code>pqblocks-jose</code> to sign a JWT-style JWS with a hybrid ML-DSA-65 + Ed25519 signature and verify it. The token stays valid unless an attacker can forge both the post-quantum and the classical signature.</p>

## The problem

JWTs are usually signed with RS256 (RSA) or ES256 (ECDSA). Shor's algorithm breaks both, so an attacker with a cryptographically relevant quantum computer could forge tokens for any user. Unlike encrypted data, signatures cannot be "harvested now" and broken later, but long-lived keys and trust anchors need to move before such a machine exists, and verifiers need time to roll out. ML-DSA (FIPS 204) is the NIST standard replacement. Pairing it with Ed25519 keeps tokens safe even if one of the two schemes turns out to be weaker than expected.

## Install

=== "pip"

    ```bash
    pip install git+https://github.com/PQBlocks/hybrid-jose
    ```

=== "uv"

    ```bash
    uv add git+https://github.com/PQBlocks/hybrid-jose
    ```

`pqblocks-jose` uses [liboqs](https://openquantumsafe.org/liboqs/) for ML-DSA and ML-KEM; see the [package page](../packages/jose.md#install) for the native library.

## Complete working code

```python title="jwt_ml_dsa.py"
--8<-- "recipes/code/jwt_ml_dsa.py"
```

Output:

```text
verified: True | token bytes: 4645
wrong key rejected: InvalidTokenError
```

## How it works

1. **The policy pins the algorithms.** `Policy` names the signature (`MLDSA65+Ed25519`), the KEM, the KDF and a maximum token size. A token whose header asks for anything else is refused, which closes the classic JWT `alg` confusion attacks.
2. **One key pair, two schemes.** `generate_keypair("ML-DSA-65-Ed25519")` returns a composite key: an Ed25519 key and an ML-DSA-65 key, concatenated. Without a `seed` argument the key material comes from `os.urandom`.
3. **Both signatures must verify.** `decode_jws` checks the ML-DSA-65 signature and the Ed25519 signature. If either fails, the token is rejected.

## Things to know

!!! warning "Tokens get bigger"
    An ML-DSA-65 signature is 3,309 bytes, so a signed token is about 4.6 KB here, against a few hundred bytes for ES256. Check header-size limits on proxies and load balancers (`max_token_bytes` enforces your own limit).

- Never pass a `seed` in production. Seeds exist so tests are reproducible.
- Keep the private key in a secret store or HSM and load it at start-up; the recipe generates one in memory only to stay self-contained.
- `pqblocks-jose` is pre-1.0 and not independently audited. Read its [security notes](https://github.com/PQBlocks/hybrid-jose/blob/main/SECURITY_NOTES.md).

## Related

- [How to add post-quantum tokens to FastAPI](fastapi-pqc.md)
- [`pqblocks-jose` package page](../packages/jose.md)
- [`pqblocks-jwe-audit`](../packages/jwe-audit.md): audit which JOSE algorithms your gateway accepts
