from pqblocks_jose import Policy, generate_keypair, encode_jws, decode_jws, encrypt_jwe, decrypt_jwe

# 1. Define an enforceable policy
policy = Policy(
    version=1,
    kem="X25519+MLKEM768",           # Hybrid KEM for JWE
    sig="MLDSA65+Ed25519",           # Hybrid signature for JWS
    kdf="HKDF-SHA256",               # Mandatory KDF enforcement
    max_token_bytes=8192,            # Header-safe limit
    kdf_info="JOSE_PostQuantum_Traditional_Hybrid X25519MLKEM768",
    sig_alg_std="ML-DSA-65-Ed25519"
)

# 2. Generate hybrid keypairs
sign_keypair = generate_keypair("ML-DSA-65-Ed25519", seed=12345)
enc_keypair = generate_keypair("X25519+MLKEM768", seed=12345)

# 3. Sign & verify a JWS token
payload = {"sub": "alice@example.com", "iat": 1700000000, "aud": "api.internal"}
jws_result = encode_jws(payload, policy, private_key=sign_keypair.private_key)

# Verify with public key
verification = decode_jws(
    token=jws_result.compact_serialization,
    policy=policy,
    public_key=sign_keypair.public_key
)
print(f"JWS verified: {verification.signature_verified}")
print(f"JWS token size: {len(jws_result.compact_serialization)} bytes")

# 4. Encrypt & decrypt a JWE token
plaintext = b"session_key:random123nonce"
jwe_result = encrypt_jwe(plaintext, policy, public_key=enc_keypair.public_key)

# Decrypt with private key
decryption = decrypt_jwe(
    token=jwe_result.compact_serialization,
    policy=policy,
    private_key=enc_keypair.private_key
)
print(f"JWE decrypted matches: {decryption.plaintext == plaintext}")
