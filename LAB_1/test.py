from dimacs import *
from dijkstra import *

import os
directory = r"graphs-lab1"

for graph in os.listdir(directory):
    with open(os.path.join(directory, graph)) as f:
        print(f"TESTING GRAPH: {graph}")
        (V,L) = loadWeightedGraph(f"graphs-lab1/{graph}")
        G = [[] for _ in range(V)]
        for u, v, c in L:
            u -= 1
            v -= 1
            G[u].append((v,c))
            G[v].append((u,c))

        read_sol = readSolution(f"graphs-lab1/{graph}")
        my_sol = getSolution(G,0)

        print(read_sol)
        print(my_sol)
        
        if my_sol == read_sol: print("PASSED")
        else: print("WRONG")