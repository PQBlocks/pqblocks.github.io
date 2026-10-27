# Interoperability Packages

Carrying larger post-quantum keys, ciphertexts, and signatures across standard protocols, wire formats, tokens, and certificates.

---

## pqblocks-jwe
- **Repository:** [`PQBlocks/hybrid-jwe`](https://github.com/PQBlocks/hybrid-jwe)
- **Standard:** RFC 7516 (JWE), FIPS 203 (ML-KEM-768), RFC 7748 (X25519)
- **Install:** `pip install pqblocks-jwe`

Compact five-part base64url-encoded JSON Web Encryption tokens with hybrid ML-KEM-768 + X25519 key encapsulation.

```python
from pqblocks_jwe import encrypt_jwe, decrypt_jwe, generate_hybrid_keypair

priv, pub = generate_hybrid_keypair()
token = encrypt_jwe(b"Confidential payload", pub)
decrypted = decrypt_jwe(token, priv)
```

---

## pqblocks-jose
- **Repository:** [`PQBlocks/hybrid-jose`](https://github.com/PQBlocks/hybrid-jose)
- **Standard:** RFC 7515 (JWS), RFC 7516 (JWE), FIPS 204 (ML-DSA-65)
- **Install:** `pip install pqblocks-jose`

Hybrid JWS signing with dual ML-DSA-65 + Ed25519 signatures, ensuring classical validation compatibility alongside post-quantum integrity.

---

## pqblocks-tls-interop
- **Repository:** [`PQBlocks/tls-hybrid-interop`](https://github.com/PQBlocks/tls-hybrid-interop)
- **Standard:** RFC 8446 (TLS 1.3), `draft-ietf-tls-hybrid-design-09` (X25519MLKEM768)
- **Install:** `pip install pqblocks-tls-interop`

Validation test suite and parser verifying TLS 1.3 ClientHello, ServerHello, and KeyShare extensions for the hybrid X25519MLKEM768 named group (0x11ec).

---

## pqblocks-csr-pop
- **Repository:** [`PQBlocks/mlkem-csr-pop`](https://github.com/PQBlocks/mlkem-csr-pop)
- **Standard:** RFC 2986 (PKCS#10), RFC 4210 (CMP)
- **Install:** `pip install pqblocks-csr-pop`

Interactive Proof-of-Possession (POP) challenge/response protocol for generating Certificate Signing Requests (CSR) with ML-KEM encryption keys.

---

## pqblocks-wire
- **Repository:** [`PQBlocks/pqc-wireformat`](https://github.com/PQBlocks/pqc-wireformat)
- **Standard:** Length-Prefixed Binary Protocol
- **Install:** `pip install pqblocks-wire`

Compact, deterministic binary container format encoding algorithm identifiers, public keys, ciphertexts, and signatures without ASN.1 overhead.
