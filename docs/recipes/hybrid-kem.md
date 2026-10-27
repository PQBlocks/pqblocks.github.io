# How to Do Hybrid X25519 + ML-KEM-768 Key Exchange

Learn how to negotiate a shared secret between two parties using hybrid key encapsulation combining **ML-KEM-768** (FIPS 203) and **X25519** (RFC 7748).

## The Problem

Traditional Diffie–Hellman exchanges (X25519, ECDH) are vulnerable to store-now-decrypt-later attacks. Standardizing purely on ML-KEM before widespread deployment carries algebraic risk. Hybrid key exchange provides both classical assurance and quantum resistance.

## Installation

```bash
pip install pqblocks-core
```

## Complete Working Code

```python
from pqblocks_core import HybridKEM

# Both parties agree on the standard hybrid mechanism
kem = HybridKEM.standard_768()

# --- Receiver (Bob) ---
bob_public_key, bob_private_key = kem.keygen()

# Bob sends bob_public_key to Alice over the network
print("Bob Public Key size:", len(bob_public_key), "bytes")

# --- Sender (Alice) ---
# Alice encapsulates a new shared secret against Bob's public key
ciphertext, alice_shared_secret = kem.encapsulate(bob_public_key)

# Alice transmits ciphertext back to Bob
print("Encapsulated Ciphertext size:", len(ciphertext), "bytes")

# --- Receiver (Bob) ---
# Bob decapsulates using his private key
bob_shared_secret = kem.decapsulate(ciphertext, bob_private_key)

# Verify both sides derived the exact same secret
assert alice_shared_secret == bob_shared_secret
print("Successfully negotiated shared secret:", alice_shared_secret.hex()[:32], "...")
```

## Security Notes

- The resulting shared secret is mixed through HKDF-SHA256, combining entropy from both algorithms.
- Always destroy/zeroize the raw shared secret from memory once symmetric encryption session keys are derived.
