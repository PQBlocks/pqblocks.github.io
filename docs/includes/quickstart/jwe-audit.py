from pqblocks_jwe_audit import audit_jwe, ComplianceStandard

# Inspect an incoming JWE compact token
jwe_token = "eyJhbGciOiJSU0EtT0FFUC0yNTYiLCJlbmMiOiJBMjU2R0NNIn0.dummy_key.dummy_iv.dummy_ct.dummy_tag"

result = audit_jwe(jwe_token, standards=[ComplianceStandard.CNSA_2_0])

print(f"Compliant: {result.compliant}")
print(f"Flagged Algorithms: {result.flagged_algorithms}")
# Compliant: False
# Flagged Algorithms: ['RSA-OAEP-256']
