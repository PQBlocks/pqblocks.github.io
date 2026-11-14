"""Solve a small Max-Cut problem with Simulated Bifurcation (pqblocks-bifurcation).

Quantum-inspired classical optimisation: not cryptography, no security claim.
Max-Cut maps to an Ising model with J_ij = w_ij; the cut value of spins s is sum w_ij (1 - s_i s_j) / 2.
"""
import itertools

import numpy as np
from pqblocks_bifurcation.solver import SimulatedBifurcationSampler

# A 6-node ring with one chord; every edge has weight 1.
edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3)]
n = 6
W = np.zeros((n, n))
for i, j in edges:
    W[i, j] = W[j, i] = 1.0


def cut_value(spins):
    return sum(W[i, j] * (1 - spins[i] * spins[j]) / 2 for i, j in edges)


# A heuristic: take the best of several independent reads.
best_spins = max((SimulatedBifurcationSampler(seed=s, mode="dSB").sample_ising(W, np.zeros(n))[0]
                  for s in range(8)), key=cut_value)
found = cut_value(best_spins)

# The graph is tiny, so brute force tells us whether the heuristic reached the optimum.
optimum = max(cut_value(np.array(b)) for b in itertools.product((-1, 1), repeat=n))
print("partition:", best_spins.tolist(), "| cut:", found, "| optimum:", optimum)
assert found <= optimum
