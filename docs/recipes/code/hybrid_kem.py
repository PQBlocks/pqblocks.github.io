"""Hybrid X25519 + ML-KEM-768 key establishment with an HKDF-SHA256 combiner (pqblocks-primitives)."""
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import x25519
from pqblocks_primitives import hybrid_decaps, hybrid_encaps, kem_keygen

raw = serialization.Encoding.Raw

# Recipient: one ML-KEM-768 key pair and one X25519 key pair, concatenated.
kem_pk, kem_sk = kem_keygen("768")
x_sk = x25519.X25519PrivateKey.generate()
x_pk = x_sk.public_key().public_bytes(raw, serialization.PublicFormat.Raw)
x_sk_bytes = x_sk.private_bytes(raw, serialization.PrivateFormat.Raw, serialization.NoEncryption())
public_key = kem_pk + x_pk            # 1184 + 32 bytes
private_key = kem_sk + x_sk_bytes     # 2400 + 32 bytes

# Sender: encapsulate to the recipient's hybrid public key.
sent = hybrid_encaps(public_key, "768", kdf="HKDF-SHA256")
ciphertext = sent.serialize()         # 1088 + 32 bytes on the wire

# Recipient: decapsulate. Both sides now hold the same 32-byte secret.
received = hybrid_decaps(private_key, ciphertext, "768", kdf="HKDF-SHA256")
assert received == sent.shared_secret
print("public key", len(public_key), "B | ciphertext", len(ciphertext), "B | shared secret", len(received), "B")
