from pqblocks_primitives import kem_keygen, kem_encaps, kem_decaps

# Generate ML-KEM-768 keypair
pk, sk = kem_keygen("768")

# Encapsulate shared secret
ct, shared_secret_sender = kem_encaps(pk, "768")

# Decapsulate shared secret
shared_secret_receiver = kem_decaps(sk, ct, "768")

assert shared_secret_sender == shared_secret_receiver
