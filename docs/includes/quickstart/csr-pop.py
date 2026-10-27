import datetime
from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.x509.oid import NameOID

from pqblocks_csr_pop.csr_builder import build_csr_with_pop, parse_csr, verify_csr_signature
from pqblocks_csr_pop.mlkem import mlkem_keygen

# 1. Attestor Identity (e.g. Host/Device Ed25519 key)
attestor_key = ed25519.Ed25519PrivateKey.generate()
ca_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Device Attestor")])
now = datetime.datetime.now(datetime.timezone.utc)
attestor_cert = (
    x509.CertificateBuilder()
    .subject_name(ca_name).issuer_name(ca_name)
    .public_key(attestor_key.public_key())
    .serial_number(x509.random_serial_number())
    .not_valid_before(now - datetime.timedelta(days=1))
    .not_valid_after(now + datetime.timedelta(days=365))
    .sign(attestor_key, None)
)

# 2. Generate ML-KEM Keypair (FIPS 203 ML-KEM-768)
ek, dk = mlkem_keygen("ML-KEM-768")

# 3. Construct PKCS#10 CSR with RFC 9883 PoP Extension
subject = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "pqc-server.internal.net")])
csr_der = build_csr_with_pop(ek, "ML-KEM-768", subject, attestor_key, attestor_cert)

# 4. CA parses CSR and verifies PoP signature
parsed = parse_csr(csr_der)
valid = verify_csr_signature(csr_der, attestor_cert)
assert valid
print(f"CSR verified successfully: {len(csr_der)} bytes DER")
