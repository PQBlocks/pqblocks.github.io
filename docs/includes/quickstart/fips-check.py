from pqblocks_fips_check import (
    hybrid_encap,
    hybrid_decap,
    sign,
    verify_sig,
    generate_cbom,
    PQCUnavailableError,
)
from pqblocks_fips_check.hybrid import hybrid_keygen

# 1. Hybrid key exchange (X25519 + ML-KEM-768)
alice_pk, alice_sk = hybrid_keygen()
bob_pk, bob_sk = hybrid_keygen()

# Alice encapsulates shared secret for Bob
ct, ss_alice = hybrid_encap(bob_pk, b"session-context")

# Bob decapsulates the ciphertext
_, ss_bob = hybrid_decap(bob_sk, ct)
assert ss_alice == ss_bob

# 2. ML-DSA-65 signature with context binding
sig = sign(b"Critical message payload", context=b"audit-auth")
assert verify_sig(b"Critical message payload", sig, context=b"audit-auth")

# 3. Export SPDX CBOM
cbom_json = generate_cbom()
assert "ML-KEM-768" in cbom_json and "ML-DSA-65" in cbom_json
