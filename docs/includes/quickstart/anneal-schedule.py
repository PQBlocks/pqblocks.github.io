import numpy as np
from pqblocks_anneal_schedule import (
    compute_instance_stats,
    generate_schedule,
    simulated_annealing,
)

# Define a 4-spin Ising ring
J = np.array([
    [0.0, -1.0,  0.0,  1.0],
    [-1.0,  0.0, -1.0,  0.0],
    [0.0, -1.0,  0.0, -1.0],
    [1.0,  0.0, -1.0,  0.0]
], dtype=float)
h = np.zeros(4, dtype=float)

# Extract graph statistics and synthesize adaptive schedule
stats = compute_instance_stats(J, h)
schedule = generate_schedule(stats, n=4, max_degree=2, budget_steps=64)

# Execute simulated annealing
result = simulated_annealing(J, h, schedule, seed=42, num_steps=64, num_runs=1)

print(f"Best Energy: {result.best_energy:.6f}")
print("Best Config:", result.best_config)
