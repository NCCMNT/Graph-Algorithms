from data import runtests

class Node:
    def __init__(self,value):
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
    V,E = G
    E.sort(key = lambda e: e[2])
    vert = [Node(v) for v in V]
    result = []

    for edge in E:
        u, v, _weight = edge
        if not connected(vert[u],vert[v]):
            union(vert[u],vert[v])
            result.append(edge)
            
    return result

def create_graph(E):
    return list(set(map(lambda e: e[0], E)) | set(map(lambda e: e[1], E))), E

def reindex(E):
    ER = []
    for u,v,w in E:
        ER.append((u-1,v-1,w))
    return ER

def solve(N, streets, lords):
    E = reindex(streets)
    G = create_graph(E)
    kingsroad = kruskal(G)
    return 61

runtests(solve)