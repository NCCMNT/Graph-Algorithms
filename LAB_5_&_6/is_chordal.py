from lexBFS import LexBFS, make_graph
from tests.tester import run_tests

def PEO(order:list, G):
        n = len(order)
        RN = dict()
        parent = [None] * (n+1)
        for i in range(n):
            v = order[i]
            RN[v] = []
            for j in range(i):
                if order[j] in G[v].out: RN[v].append(order[j])
            if i != 0: parent[v] = RN[v][-1]

        for i in range(1,n):
            v = order[i]
            if not ((set(RN[v]) - set([parent[v]])) <= set(RN[parent[v]])): return False
        return True

def is_chordal(A):
    V, L = A
    G = make_graph(V,L)
    return int(PEO(LexBFS(G), G))

if __name__ == '__main__':
    run_tests(4, is_chordal, graph_converter='raw', subdir='chordal')