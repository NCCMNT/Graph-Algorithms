from tests.tester import run_tests

class Node:
    def __init__(self, value):
        self.val = value
        self.parent = self
        self.rank = 0

def find(x:Node):
    if x.parent != x: x.parent = find(x.parent)
    return x.parent

def union(x:Node, y:Node):
    x = find(x)
    y = find(y)
    if x == y: return
    if x.rank > y.rank: y.parent = x
    else:
        x.parent = y
        if x.rank == y.rank: y.rank += 1

def connected(x,y):
    return find(x) == find(y)

def kruskal(G):
    n,E = G
    V = [i for i in range(n+1)]
    E.sort(key = lambda e: e[2], reverse = True)
    vert = [Node(v) for v in V]
    result = [[] for _ in range(n+1)]

    for edge in E:
        if connected(vert[0], vert[1]): break

        u, v, c = edge

        if not connected(vert[u],vert[v]):
            union(vert[u],vert[v])
            result[u].append((v-1,c))
            result[v].append((u-1,c))

    result.pop(0)
    return result

def DFS_iterative(G, s, t):
    stack = [(s, [])]  # Stack holds tuples of (current node, path to current node)
    visited = set()
    
    while stack:
        u, path = stack.pop()
        if u == t:
            return path  # Return the path when destination is reached
        if u not in visited:
            visited.add(u)
            for v, cost in G[u]:
                if v not in visited:
                    # Append the new edge to the path
                    stack.append((v, path + [(u, v, cost)]))
    
    return None

def printSolution(G):
    max_spanning_tree = kruskal(G)
    path = DFS_iterative(max_spanning_tree, 0, 1)

    if path is None:
        return None
    result = min(edge[2] for edge in path)
    return result



run_tests(1, printSolution, graph_converter = 'set')