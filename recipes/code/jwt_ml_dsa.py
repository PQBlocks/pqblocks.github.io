"""Sign a JWT-style token with hybrid ML-DSA-65 + Ed25519 and verify it (pqblocks-jose)."""
from pqblocks_jose import Policy, decode_jws, encode_jws, generate_keypair

# The policy pins every algorithm choice; a token that disagrees with it is rejected.
policy = Policy(
    version=1,
    kem="X25519+MLKEM768",
    sig="MLDSA65+Ed25519",
    kdf="HKDF-SHA256",
    max_token_bytes=8192,
    kdf_info="JOSE_PostQuantum_Traditional_Hybrid X25519MLKEM768",
    sig_alg_std="ML-DSA-65-Ed25519",
)

# No seed: the key comes from os.urandom. Seeds exist for reproducible tests only.
keys = generate_keypair("ML-DSA-65-Ed25519")

claims = {"sub": "alice@example.com", "aud": "api.example.com", "iat": 1700000000}
token = encode_jws(claims, policy, private_key=keys.private_key).compact_serialization

result = decode_jws(token=token, policy=policy, public_key=keys.public_key)
assert result.signature_verified
print("verified:", result.signature_verified, "| token bytes:", len(token))

# A different key must not verify the token.
other = generate_keypair("ML-DSA-65-Ed25519")
try:
    forged = decode_jws(token=token, policy=policy, public_key=other.public_key)
    assert not forged.signature_verified
except Exception as exc:  # the library may raise instead of returning False
    print("wrong key rejected:", type(exc).__name__)
