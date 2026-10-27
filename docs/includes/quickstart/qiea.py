import numpy as np
from pqblocks_qiea import solve_ising

# 4-spin antiferromagnetic ring
N = 4
h = np.zeros(N)
J = np.zeros((N, N))
for i in range(N):
    j = (i + 1) % N
    J[i, j] = J[j, i] = 1.0

# Solve using QIEA
best_spins, best_energy = solve_ising(
    h=h,
    J=J,
    num_generations=100,
    seed=42
)

print("Best Spin State:", best_spins.tolist())
print(f"Best Energy: {best_energy:.6f}")
