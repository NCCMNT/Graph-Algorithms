import networkx as nx
from tests.tester import run_tests

def max_flow(A):
    V, L = A
    G = nx.DiGraph()
    G.add_nodes_from( [i for i in range(1, V+1)] )
    for u, v, w in L:
        G.add_edge(u,v, capacity = w)

    return nx.algorithms.flow.maximum_flow(G, 1, V)[0]

if __name__ == '__main__':
    run_tests(2, max_flow, graph_converter='raw', subdir='flow')