from lexBFS import LexBFS, make_graph
from tests.tester import run_tests

def check_RN(G):
    O = LexBFS(G)
    n = len(O)
    max_RN = 0

    for i in range(n):
        v = O[i]
        current_RN = 1

        for j in range(i):
            if O[j] in G[v].out:
                current_RN += 1
        
        max_RN = max(max_RN, current_RN)
    
    return max_RN

def max_clique(A):
    V, L = A
    G = make_graph(V,L)
    return check_RN(G)

run_tests(4, max_clique, graph_converter='raw', subdir='maxclique')
