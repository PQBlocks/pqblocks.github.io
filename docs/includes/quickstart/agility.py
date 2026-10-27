import json
from pqblocks_agility.cbom import parse_cbom_dict
from pqblocks_agility.cli import compute_cars_score

cbom_data = {
    "bomFormat": "CycloneDX", "specVersion": "1.6",
    "serialNumber": "urn:uuid:6c361972-23c3-4d4b-9721-a47fa266184a", "version": 1,
    "components": [{"type": "cryptographic-asset", "name": "ML-KEM-768",
                    "properties": [{"name": "pqblocks-scan.algorithm", "value": "ML-KEM-768"},
                                   {"name": "pqblocks-scan.grade", "value": "A"}]}]
}
score, dims = compute_cars_score(parse_cbom_dict(cbom_data))
print(f"CARS score: {score:.1f} / 100.0 (Grade A)")
