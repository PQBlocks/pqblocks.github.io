from pqblocks_anneal_sqa import SimulatedQuantumAnnealingSampler

# 1. Define 4-spin Ising problem
h = [-1.0, 1.0, 2.0, -2.0]
J = [
    [0.0, 1.0, -1.0, 2.0],
    [0.0, 0.0, 1.0, -1.0],
    [0.0, 0.0, 0.0, -2.0],
    [0.0, 0.0, 0.0, 0.0],
]

# 2. Initialize SQA solver
sampler = SimulatedQuantumAnnealingSampler()

# 3. Sample Ising ground state
samples, energies = sampler.sample_ising(h, J, num_sweeps=1000, beta=5.0, P=32)

print("Best Spin State:", samples[0].tolist())
print(f"Best Energy: {energies[0]:.6f}")
