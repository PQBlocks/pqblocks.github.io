---
title: How to solve Max-Cut with a quantum-inspired solver in Python
description: Solve a Max-Cut graph partitioning problem as an Ising model with Simulated Bifurcation (pqblocks-bifurcation) and check it against brute force. Tested code.
---

# How to solve Max-Cut with a quantum-inspired solver

<p class="pqb-lead">Map a Max-Cut graph problem to an Ising model and solve it with Simulated Bifurcation, a classical algorithm modelled on the dynamics of a quantum bifurcation machine. Uses <code>pqblocks-bifurcation</code>.</p>

!!! warning "Not cryptography"
    Quantum-inspired classical optimisation: not cryptography, no security claim.

## The problem

Max-Cut splits the nodes of a graph into two groups so that the total weight of edges between the groups is as large as possible. It is NP-hard and appears in circuit layout, clustering and portfolio problems. Many such problems can be written as an Ising model or a QUBO, and quantum-inspired heuristics find good solutions quickly on an ordinary CPU.

## Install

```bash
pip install git+https://github.com/PQBlocks/simulated-bifurcation
```

## Complete working code

```python title="qubo_maxcut.py"
--8<-- "recipes/code/qubo_maxcut.py"
```

Output:

```text
partition: [-1, 1, -1, 1, -1, 1] | cut: 7.0 | optimum: 7.0
```

## How it works

1. Each node gets a spin `s_i = ±1`, which says which side of the cut it is on.
2. With couplings `J_ij = w_ij`, minimising the Ising energy `Σ J_ij s_i s_j` maximises the cut `Σ w_ij (1 − s_i s_j) / 2`.
3. Simulated Bifurcation (Goto et al., *Science Advances* 2019 and 2021) evolves continuous oscillators that bifurcate into ±1 states. The discrete variant (`mode="dSB"`) is used here.
4. It is a heuristic: take the best of several independent reads (different seeds). On this small graph, brute force confirms the optimum was reached.

## Things to know

- For graphs beyond a few dozen nodes brute force is impossible. Compare solvers with [`pqblocks-qubo-bench`](../packages/qubo-bench.md) (time-to-solution).
- Build and convert QUBO / Ising models with [`pqblocks-qubo`](../packages/qubo.md).

## Related

- [Quantum-inspired packages](../packages/optimization.md)
