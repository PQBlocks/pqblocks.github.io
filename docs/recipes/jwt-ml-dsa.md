# How to Sign and Verify JWTs with ML-DSA in Python

Learn how to create and verify digital signatures on JSON Web Tokens using NIST's standardized **ML-DSA-65** (FIPS 204) and **Ed25519**.

## The Problem

Classical digital signatures like RSA and ECDSA can be forged by a quantum computer running Shor's algorithm. Switching to hybrid post-quantum signatures ensures long-term integrity and authenticity.

## Installation

```bash
pip install pqblocks-jose
```

## Complete Working Code

```python
from pqblocks_jose import sign_jws, verify_jws, generate_signing_keypair

# 1. Generate hybrid signing keypair (ML-DSA-65 + Ed25519)
signing_key, verify_key = generate_signing_keypair()

# 2. Define claims payload
claims = {
    "sub": "service-worker-99",
    "permissions": ["deploy:release", "read:telemetry"],
    "iss": "https://auth.example.com"
}

# 3. Create compact signed JWS token
token = sign_jws(claims, signing_key)
print("Signed Post-Quantum JWS Token:\n", token)

# 4. Verify token and decode claims
verified_payload = verify_jws(token, verify_key)
print("\nVerified Claims:", verified_payload)
assert verified_payload["sub"] == "service-worker-99"
```

## How It Works

- The signing operation computes signatures with both **ML-DSA-65** (lattice-based) and **Ed25519** (Edwards curve).
- The resulting JWS compact token carries both cryptographic proofs in its signature segment.
- `verify_jws` validates both mathematical signatures before trusting the payload.
