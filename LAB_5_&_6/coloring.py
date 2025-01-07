from lexBFS import LexBFS, make_graph
from tests.tester import run_tests

def find_next_minimal_color(used):
    n = len(used)
    is_present = [False] * (n + 1)

    for num in used:
        if 1 <= num <= n:
            is_present[num] = True

    for i in range(1, n + 1):
        if not is_present[i]:
            return i

    return n + 1

def solve(G):
    n = len(G)
    O = LexBFS(G)
    color = [0] * (n+1)

    for i in O:
        v = G[i]
        used_colors = {color[u] for u in v.out}
        c = find_next_minimal_color(used_colors)
        color[v.idx] = c

    return max(color)

def coloring(A):
    V, L = A
    G = make_graph(V,L)
    return solve(G)

run_tests(4, coloring, graph_converter='raw', subdir='coloring')