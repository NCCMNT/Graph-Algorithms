from data import runtests

class Node:
    def __init__(self,value):
        self.val = value
        self.parent = self
        self.rank = 0
    def __repr__(self):
        return f'{self.val}'

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
    vert = [Node(v) for v in range(V+1)]
    result = []

    for edge in E:
        u, v, _weight = edge
        if not connected(vert[u],vert[v]):
            union(vert[u],vert[v])
            result.append(edge)
            
    return result

class Vertex:
  def __init__(self, idx):
    self.idx = idx
    self.out = set()

  def connect_to(self, v):
    self.out.add(v)
    
def make_graph(V,L):
	G = [None] + [Vertex(i) for i in range(1, V+1)]

	for (u, v, w) in L:
		G[u].connect_to((v,w))
		G[v].connect_to((u,w))
    
	return G

def find_lords_road(lord:list, G:list[Vertex]):

    def DFS(start, end, G:list[Vertex]):
        V = len(G) - 1
        visited = [False] * (V+1)
        stack = [(start, [])]
        
        while stack:
            u, path = stack.pop()
            if not visited[u]:
                visited[u] = True
                if u == end: return path
                for v, w in G[u].out:
                    if not visited[v]:
                        stack.append((v, path + [(min(u,v),max(u,v),w)]))
            
        return None

    n = len(lord)
    road = set()
    for i in range(n-1):
        road |= set(DFS(lord[i], lord[i+1], G))
    return road

def sum_strength(road):
    result = 0
    for _,_,w in road:
        result += w
    return result

def get_vertices(S):
    result = set(map(lambda e: e[0], S)) | set(map(lambda e: e[1], S))
    return result

class Lord:
  def __init__(self, idx):
    self.idx = idx
    self.out = set()

  def connect_to(self, v):
    self.out.add(v)

def make_graph_of_lords(V,L):
    G = [None] + [Lord(i) for i in range(1, V+1)]
    for (u, v) in L:
        G[u].connect_to(v)
        G[v].connect_to(u)
    return G

from collections import defaultdict

def edge_list_to_adjacency_list(edges):
    adjacency_list = defaultdict(set)
    for u, v in edges:
        adjacency_list[u].add(v)
        adjacency_list[v].add(u)
    return adjacency_list

def bron_kerbosch(R, P, X, adjacency_list, cliques):
    if not P and not X:  # Warunek zakończenia - znaleźliśmy klikę
        cliques.append(R)
        return
    
    for v in list(P):
        bron_kerbosch(
            R | {v}, 
            P & adjacency_list[v], 
            X & adjacency_list[v], 
            adjacency_list, 
            cliques
        )
        P.remove(v)
        X.add(v)

def find_maximum_cliques(edges):
    adjacency_list = edge_list_to_adjacency_list(edges)
    cliques = []
    bron_kerbosch(set(), set(adjacency_list.keys()), set(), adjacency_list, cliques)
    max_size = max(len(clique) for clique in cliques)
    return [clique for clique in cliques if len(clique) == max_size]

def solve(N, streets, lords):
    G = (N,streets)
    kingsroad = kruskal(G)
    KR = make_graph(N, kingsroad)
    
    n = len(lords)
    all_lords_roads = []
    for i in range(n):
        lord = lords[i]
        lord_road = find_lords_road(lord,KR)
        lord_strength = sum_strength(lord_road)
        lord_castles = get_vertices(lord_road)
        all_lords_roads.append((lord_road, lord_strength, lord_castles))

    if n == 1: return all_lords_roads[0][1]
    all_lords_roads.sort(key = lambda x: x[1], reverse = True)

    L = set()
    for i in range(n):
        for j in range(n):
            if i == j: continue
            edges_a, _, vertices_a = all_lords_roads[i]
            edges_b, _, vertices_b  = all_lords_roads[j]
            if (edges_a & edges_b == set()) and (vertices_a & vertices_b == set()):
                L.add((min(i, j), max(i, j)))

    anticollision_graph = list(L)

    cliques = find_maximum_cliques(anticollision_graph)

    result = 0
    for clique in cliques:
        pres = 0
        list_of_lords = list(clique)
        for i in list_of_lords:
            pres += all_lords_roads[i][1]
        result = max(result, pres)
    return result

# A = solve(6,[
#     (1, 2, 4),
#     (2, 3, 5),
#     (3, 4, 6),
#     (4, 5, 8),
#     (5, 6, 7),
#     (1, 6, 9),
#     (2, 5, 10),
#   ],[
#     [1, 3],
#     [2, 5],
#     [4, 6],
#   ])
# print(A)
# A = solve(4, [
#   (1, 2, 2),
#   (2, 3, 3),
#   (2, 4, 5),
#   ],
#   [
#     [1, 3, 4],
#   ])

# A = solve(4, [
#   (1, 2, 5),
#   (2, 3, 4),
#   (3, 4, 6),
#   ],
#   [
#     [1, 2],
#     [3, 4],
#   ])
# print(A)

# A = solve(12, [
#     (1, 2, 21),
#     (2, 3, 23),
#     (3, 4, 22),
#     (4, 5, 25),
#     (3, 5, 29),
#     (5, 7, 26),
#     (7, 8, 22),
#     (8, 9, 18),
#     (4, 6, 24),
#     (3, 6, 27),
#     (6, 10, 19),
#     (10, 11, 20),
#     (11, 12, 21),
#     (5, 6, 29),
#     (7, 10, 30),
#     (8, 11, 31),
#     (9, 12, 32),
#   ],
#   [
#     [1, 3],
#     [2, 4],
#     [5, 11],
#     [6, 8],
#     [7, 9],
#     [10, 12],
#   ])
# print(A)
runtests(solve)