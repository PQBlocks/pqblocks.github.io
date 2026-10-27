import numpy as np
from pqblocks_anneal_sa import simulated_annealing

# 1. Define 4-spin Ising problem (couplings J and linear biases h)
J = np.array([
    [0.0, 1.0, -1.0, 0.0],
    [1.0, 0.0, 1.0, -1.0],
    [-1.0, 1.0, 0.0, 1.0],
    [0.0, -1.0, 1.0, 0.0],
])
h = np.array([0.5, -0.3, 0.2, -0.1])

# 2. Solve with auto-derived parameters
result = simulated_annealing(J, h, num_sweeps=100, num_reads=10, seed=42)

# 3. Retrieve best solution
best_idx = np.argmin(result["energies"])
print(f"Best energy: {result['energies'][best_idx]:.6f}")
print(f"Sample: {result['samples'][best_idx].tolist()}")
