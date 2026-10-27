# Quantum-Inspired Optimization Packages

> **Important Disclaimer:** These packages provide classical combinatorial optimization algorithms modelled on quantum dynamics (Ising models, annealing, bifurcation). They run entirely on classical hardware (CPU/GPU) and provide **zero cryptographic security**. They are maintained strictly separate from PQBlocks cryptographic libraries.

---

## pqblocks-bifurcation
- **Repository:** [`PQBlocks/simulated-bifurcation`](https://github.com/PQBlocks/simulated-bifurcation)
- **Algorithm:** Ballistic (bSB) and Discrete (dSB) Simulated Bifurcation (Goto et al.)
- **Install:** `pip install pqblocks-bifurcation`

Heuristic solver solving large-scale NP-hard Ising and QUBO combinatorial optimization problems (such as Max-Cut and portfolio allocation) up to thousands of spins.

```python
import numpy as np
from pqblocks_bifurcation import SimulatedBifurcationSampler

# 4-spin frustrated ring
J = np.array([
    [0.0, 1.0, 0.0, 1.0],
    [1.0, 0.0, 1.0, 0.0],
    [0.0, 1.0, 0.0, 1.0],
    [1.0, 0.0, 1.0, 0.0]
])
h = np.zeros(4)

sampler = SimulatedBifurcationSampler(mode="bSB", steps=1000, seed=42)
spins, energy = sampler.sample_ising(J, h)
print(f"Optimal configuration: {spins}, Energy: {energy}")
```

---

## pqblocks-qubo
- **Repository:** [`PQBlocks/qubo-core`](https://github.com/PQBlocks/qubo-core)
- **Standard:** Quadratic Unconstrained Binary Optimization Formulation
- **Install:** `pip install pqblocks-qubo`

Unified mathematical matrix representations and conversions between QUBO, Ising, and binary quadratic models.

---

## Additional Optimization Packages

- **`pqblocks-qubo-bench`** (`PQBlocks/qubo-benchmark-harness`): Standardized benchmarking suite comparing heuristic solvers against exact CP-SAT and heuristic baselines.
- **`pqblocks-anneal-sa`** (`PQBlocks/simulated-annealing`): Classical Simulated Annealing with adaptive geometric schedules.
- **`pqblocks-anneal-sqa`** (`PQBlocks/simulated-quantum-annealing`): Path-Integral Simulated Quantum Annealing simulating transverse magnetic fields.
- **`pqblocks-digital-anneal`** (`PQBlocks/digital-annealing`): Digital Annealer-style parallel trial evaluation heuristic.
- **`pqblocks-population-anneal`** (`PQBlocks/population-annealing`): Population Annealing Monte Carlo algorithm.
- **`pqblocks-qiea`** (`PQBlocks/quantum-inspired-evolutionary`): Quantum-Inspired Evolutionary Algorithm using Q-bit representations.
- **`pqblocks-anneal-schedule`** (`PQBlocks/annealing-schedule`): Automated cooling and bifurcation schedule calculator.
