from pqblocks_fips_dualmode import CryptoEnvelope

# Initialize classical FIPS mode
env = CryptoEnvelope(mode="fips")

# Generate an ECDH P-256 keypair
key = env.generate_key()

# Encrypt sensitive payload using AES-256-GCM
plaintext = b"Sensitive transactional payload data"
aad = b"tenant-id=1084;classification=restricted"
envelope = env.encrypt(key, plaintext, associated_data=aad)

# Decrypt and verify ciphertext and authentication tag
decrypted = env.decrypt(key, envelope)
assert decrypted == plaintext
print("FIPS Mode decryption successful!")
