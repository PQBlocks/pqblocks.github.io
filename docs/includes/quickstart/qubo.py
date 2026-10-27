import networkx as nx
from pqblocks_qubo import load_maxcut, to_qubo

# 1. Build a graph and construct native Ising model for MaxCut
G = nx.cycle_graph(4)
bqm_ising = load_maxcut(G)

# 2. Convert transparently to QUBO
bqm_qubo = to_qubo(bqm_ising)

# 3. Evaluate state energy (deterministic evaluation)
sample = {0: 0, 1: 1, 2: 0, 3: 1}
print(f"QUBO Energy: {bqm_qubo.energy(sample)}")
