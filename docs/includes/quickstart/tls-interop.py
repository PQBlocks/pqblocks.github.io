from pqblocks_tls_interop import derive_shared_secret_10024, derive_key_material_rfc9954
from pqblocks_tls_interop.verifier.probe import HybridGroupProbe

# 1. Inspect RFC 10024 shared secret specifications
layout = HybridGroupProbe.get_shared_secret_layout()
print(layout["group_name"])  # X25519MLKEM768
print(layout["codepoint"])   # 4588

# 2. Derive combined hybrid shared secret (64 bytes: 32 bytes ML-KEM || 32 bytes X25519)
classical_ss = b"\x01" * 32
mlkem_ss = b"\x02" * 32
combined = derive_shared_secret_10024(classical_ss, mlkem_ss)
assert combined == mlkem_ss + classical_ss

# 3. Derive key material per RFC 9954 (48-byte SHA-384 digest)
km = derive_key_material_rfc9954(classical_ss, mlkem_ss)
assert len(km) == 48

# 4. Probe an external endpoint
probe = HybridGroupProbe("example.com", port=443, timeout=5.0)
result = probe.probe(sni="example.com")
if result.downgrade_detected:
    print(f"Warning: Endpoint downgraded to classical ({result.error_reason})")
