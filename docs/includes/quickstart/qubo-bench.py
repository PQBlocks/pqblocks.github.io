from pqblocks_qubo_bench.tts_engine import calculate_tts

# Timing data: list of (runtime_seconds, success_boolean) tuples
runs = [(0.012, True), (0.015, False), (0.011, True), (0.014, True)]

# Calculate Time-To-Solution for 99% target confidence
tts = calculate_tts(runs, target_prob=0.99)
print(f"Calculated TTS (99% target): {tts:.4f}s")
