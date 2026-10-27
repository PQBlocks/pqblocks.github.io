import numpy as np
from pqblocks_bifurcation.solver import SimulatedBifurcationSampler

sampler = SimulatedBifurcationSampler(seed=42, mode="dSB")
J = np.array([[0.0, -1.0], [-1.0, 0.0]])   # couplings
h = np.array([0.5, -0.5])                   # local fields
spins, energy = sampler.sample_ising(J, h)
print(spins, energy)                        # [1 1] -1.0
