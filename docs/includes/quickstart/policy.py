from pqblocks_policy import PolicyEngine, cnsa20_default, Asset, UsageClass

# 1. Load the default CNSA 2.0 profile
profile = cnsa20_default()
engine = PolicyEngine(profile)

# 2. Define a cryptographic asset to evaluate
asset = Asset(ref="tls-session-1", alg="ML-KEM-768+X25519", use=UsageClass.KEY_EXCHANGE)

# 3. Evaluate compliance
report = engine.evaluate([asset])
print(f"Verdict: {report.verdict.value} | Assets: {report.asset_count} | Violations: {report.violation_count}")
