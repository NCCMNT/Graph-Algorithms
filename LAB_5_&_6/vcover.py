from lexBFS import LexBFS, make_graph
from tests.tester import run_tests

def solve(G):
    O = LexBFS(G)[::-1]

    I = set()

    for i in O:
        v = G[i]
        N = v.out
        if I & N == set(): I.add(v.idx)

    return len(G) - 1 - len(I)

def vcover(A):
    V, L = A
    G = make_graph(V,L)
    return solve(G)

run_tests(4, vcover, graph_converter='raw', subdir='vcover')