from pqblocks_scan.discovery import Discovery
from pqblocks_scan.scorer import CARSScorer
from pqblocks_scan.cbom import CBOMGenerator

src = "import hashlib\nh = hashlib.sha1(b'x').hexdigest()\nfrom pqcrypto.kem import ml_kem_768\n"
assets = Discovery().discover_source(src, "app.py").assets
print([(a.algorithm, a.line_number, a.is_quantum_vulnerable) for a in assets])
# [('ML-KEM-768', 3, False), ('SHA-1', 2, True)]
grade = CARSScorer.evaluate(assets)
print(grade.score, grade.letter)                      # 55.5 C
print(CBOMGenerator.generate(assets)["specVersion"])  # 1.6
