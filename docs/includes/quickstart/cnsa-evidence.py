import hashlib
import json
from pqblocks_cnsa_evidence import (
    scan_parser,
    lockfile_parser,
    sbom_emitter,
    crypto_inventory_emitter,
    compliance_matrix_emitter,
    narrative_emitter,
    migration_scheduler,
    executive_summary_emitter,
    attestation_emitter,
)

# 1. Ingest scan findings and lockfile
scan_data = {
    "algorithms": [
        {"name": "ML-KEM-1024", "type": "key-encapsulation", "mode": "PQC", "keySize": 1024, "cnsA20Grade": "A", "breakYear": 2040},
        {"name": "RSA-2048", "type": "signature", "mode": "classical", "keySize": 2048, "cnsA20Grade": "D", "breakYear": 2030},
        {"name": "AES-256", "type": "encryption", "mode": "classical", "keySize": 256, "cnsA20Grade": "A", "breakYear": 2050},
    ],
    "tls_endpoints": [{"host": "api.fed.gov", "cipher": "TLS_AES_256_GCM_SHA384"}],
    "dependencies": [{"name": "cryptography", "version": "42.0.5"}],
    "pqc_grades": {"ML-KEM-1024": "A", "RSA-2048": "D", "AES-256": "A"}
}
lockfile_content = "cryptography==42.0.5\nrequests>=2.31.0\n"

scan_res = scan_parser(scan_data)
lock_res = lockfile_parser("python", lockfile_content)

# 2. Synthesize evidence pack components
sbom = sbom_emitter(scan_res, lock_res)
inventory = crypto_inventory_emitter(scan_res, lock_res)
matrix = compliance_matrix_emitter(scan_res)
narrative = narrative_emitter(scan_res, lock_res)
schedule = migration_scheduler(lock_res, matrix)
exec_summary = executive_summary_emitter(matrix, narrative, schedule)

def sha256(val):
    b = val.encode("utf-8") if isinstance(val, str) else json.dumps(val, sort_keys=True).encode("utf-8")
    return hashlib.sha256(b).hexdigest()

# 3. Create cryptographic attestation
attestation = attestation_emitter(
    sbom_sha256=sha256(sbom),
    inventory_sha256=sha256(inventory),
    narrative_sha256=sha256(narrative),
    compliance_sha256=sha256(matrix),
    migration_plan_sha256=sha256(schedule),
    executive_summary_sha256=sha256(exec_summary),
    tool_version="0.1.0",
    tool_timestamp="2026-10-26T00:00:00Z",
    scan_json_sha256=sha256(scan_data),
    lockfile_hashes={"requirements.txt": sha256(lockfile_content)},
)

print(f"Evidence Pack Generated: {sbom['bomFormat']} {sbom['specVersion']}")
print(f"Compliance Status: {matrix.get('status', 'complete')}")
