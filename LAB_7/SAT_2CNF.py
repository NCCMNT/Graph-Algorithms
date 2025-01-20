import networkx as nx
from tests.tester import run_tests

def SAT_2CNF(A):
    V, L = A

if __name__ == '__main__':
    run_tests(None, SAT_2CNF, graph_converter='raw', otherdir='sat')