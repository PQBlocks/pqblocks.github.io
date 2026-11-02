import numpy as np
import scipy.sparse as sp
from pqblocks_sparse_bifurcation import SparseStructureAwareDSB

# Create sparse coupling matrix (CSR)
J = sp.csr_matrix([[0, 1, 0], [1, 0, 1], [0, 1, 0]])
h = np.array([0.0, 0.0, 0.0])

solver = SparseStructureAwareDSB(num_sweeps=1000, execution_mode="csr", seed=42)
sampleset = solver.sample_ising(h, J)

print("Best energy:", sampleset.first.energy)
print("Best sample:", sampleset.first.sample)
