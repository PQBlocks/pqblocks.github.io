from pqblocks.hybrid_cert_validator import (
    HybridCertValidator,
    CompositePolicy,
    InvalidPEM,
    ValidationResult,
)

# Initialize validator with CNSA 2.0 Transition Policy
validator = HybridCertValidator(policy=CompositePolicy.CNSA20_TRANSITION)
assert validator.policy == CompositePolicy.CNSA20_TRANSITION

# Validate input with strict fail-safe exception handling
try:
    validator.validate(b"non-pem-data")
except InvalidPEM:
    pass  # Fail-safe rejection of invalid inputs
