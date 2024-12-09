from lexBFS import LexBFS, make_graph
from tests.tester import run_tests

def is_chordal(A):
    V, L = A
    G = make_graph(V,L)
    
    def PEO(O:list):
        n = len(O)
        RN = dict()
        parent = [None] * (n+1)
        for i in range(n):
            v = O[i]
            RN[v] = []
            for j in range(i):
                if O[j] in G[v].out: RN[v].append(O[j])
            if i != 0: parent[v] = RN[v][-1]

        for i in range(1,n):
            v = O[i]
            if not ((set(RN[v]) - set([parent[v]])) <= set(RN[parent[v]])): return False
        return True
    
    return int(PEO(LexBFS(G)))

run_tests(4, is_chordal, graph_converter='raw', subdir='chordal')