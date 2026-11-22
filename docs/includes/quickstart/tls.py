from pqblocks_tls import fuzz_tls_handshake, FuzzResults

# Execute 1,000 hybrid handshake iterations with a deterministic seed
results: FuzzResults = fuzz_tls_handshake(
    algorithms=("X25519", "ML-KEM-768"),
    iterations=1000,
    max_latency_ms=50,
    seed=42,
)

print(f"Passed: {results.passed}/{results.total_iterations}")
print(f"Elapsed: {results.elapsed_ms} ms")
assert results.all_passed()
