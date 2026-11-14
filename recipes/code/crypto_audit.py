"""Find quantum-vulnerable cryptography in source code and grade readiness (pqblocks-scan)."""
from pqblocks_scan.cbom import CBOMGenerator
from pqblocks_scan.discovery import Discovery
from pqblocks_scan.scorer import CARSScorer

source = '''
from cryptography.hazmat.primitives.asymmetric import rsa, ec
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
signer = ec.generate_private_key(ec.SECP256R1())
import hashlib
digest = hashlib.sha256(b"data").hexdigest()
'''

assets = Discovery().discover_source(source, "app.py").assets
for a in sorted(assets, key=lambda a: a.line_number):
    status = "QUANTUM-VULNERABLE" if a.is_quantum_vulnerable else "ok"
    print(f"app.py:{a.line_number:<3} {a.algorithm:<12} {status}")

grade = CARSScorer.evaluate(assets)
cbom = CBOMGenerator.generate(assets)
print("readiness:", grade.score, grade.letter, "| CBOM spec", cbom["specVersion"])
assert any(a.is_quantum_vulnerable for a in assets)
