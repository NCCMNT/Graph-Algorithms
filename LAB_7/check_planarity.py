import networkx as nx
from tests.tester import run_tests

def check_planarity(A):
    V, L = A
    G = nx.Graph()
    G.add_nodes_from([i for i in range(1,V+1)])
    G.add_edges_from(map(lambda x: (x[0], x[1]), L))
    # G = nx.Graph()
    # G.add_nodes_from([1,2,3,4])
    # G.add_edges_from([(1,2),(1,3),(2,3),(2,4),(3,4)])
    # print(G.number_of_nodes())
    # print(G.number_of_edges())
    # print(G.nodes)
    # print(G.edges)

    return int(nx.algorithms.planarity.check_planarity(G)[0])

if __name__ == '__main__':
    run_tests(7, check_planarity, graph_converter='raw')