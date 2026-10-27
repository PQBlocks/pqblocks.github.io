# Post-Quantum Cryptography Packages

Core post-quantum cryptographic primitives, hybrid key encapsulation mechanisms, and signature schemes.

---

## pqblocks-core
- **Repository:** [`PQBlocks/hybrid-sdk`](https://github.com/PQBlocks/hybrid-sdk)
- **Standard:** NIST FIPS 203 (ML-KEM-768/1024), FIPS 204 (ML-DSA-65/87), RFC 7748 (X25519)
- **Install:** `pip install pqblocks-core`

Unified hybrid SDK providing clean-room tested implementations of post-quantum key encapsulation and digital signatures paired with classical curves.

```python
from pqblocks_core import HybridKEM

# Initialize standard hybrid KEM (ML-KEM-768 + X25519)
kem = HybridKEM.standard_768()
pub, priv = kem.keygen()

# Encapsulate
ciphertext, secret_sender = kem.encapsulate(pub)

# Decapsulate
secret_receiver = kem.decapsulate(ciphertext, priv)
assert secret_sender == secret_receiver
```

---

## pqblocks-primitives
- **Repository:** [`PQBlocks/fips-pqc-primitives`](https://github.com/PQBlocks/fips-pqc-primitives)
- **Standard:** FIPS 203, FIPS 204, FIPS 205
- **Install:** `pip install pqblocks-primitives`

Raw bindings and direct wrapper APIs around maintained, audited reference implementations of the post-quantum primitives.
