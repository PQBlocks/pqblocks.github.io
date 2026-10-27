from pqblocks_jwe import ALG_HYBRID, ENC_A256GCM, parse_jwe, serialize_jwe

ciphertext = bytes(48)        # your AEAD output; this package does not encrypt
kem_ct = bytes(1088 + 32)     # your ML-KEM-768 ciphertext || X25519 ephemeral public key
header = {"alg": ALG_HYBRID, "enc": ENC_A256GCM, "kid": "recipient-1"}

token = serialize_jwe(ciphertext, header, {"cty": "application/json"}, b"settlement-v1", kem_ct)
parsed = parse_jwe(token)
assert parsed["header"]["alg"] == ALG_HYBRID   # parse_jwe does not check alg/enc for you
print(len(token), parsed["aad"], len(parsed["kem_ct"]))   # 1697 b'settlement-v1' 1120
