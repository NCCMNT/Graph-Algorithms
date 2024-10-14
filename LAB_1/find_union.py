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

def DFS(G, s, t, visited, path):
    if s == t: return path
    visited.add(s)
    for v, cost in G[s]:
        if v not in visited:
            result = DFS(G, v, t, visited, path + [(s,v,cost)])
            if result: return result
    return None

def printSolution(G):
    V, E = G
    max_spanning_tree = kruskal(G)
    # print(max_spanning_tree)
    visited = set()
    path = DFS(max_spanning_tree, 0, 1, visited, [])
    result = min(edge[2] for edge in path)
    return result


from tester import run_tests
run_tests(r'graphs-lab1', printSolution, 'set', runall=True, without=['pp1000','path10000', 'path1000'])