from pqblocks_qse_sdk import keypair, encapsulate, decapsulate, sign, verify

# Key encapsulation (ML-KEM-768)
pk, sk = keypair("ml-kem-768")
ct, ss_sender = encapsulate(pk, "ml-kem-768")
ss_receiver = decapsulate(sk, ct, "ml-kem-768")
assert ss_sender == ss_receiver

# Digital signature (ML-DSA-65)
pk_sig, sk_sig = keypair("ml-dsa-65")
sig = sign(sk_sig, b"sample payload", "ml-dsa-65")
valid = verify(pk_sig, sig, b"sample payload", "ml-dsa-65")
assert valid is True
print("Verified output:", valid)
