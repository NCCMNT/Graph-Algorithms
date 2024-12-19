from data import runtests
import sys
sys.setrecursionlimit(10000)

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

class Lord:
    def __init__(self, id, castles, strength):
        self.castles = castles
        self.id = id
        self.strength = strength
        self.color = None
        self.out = set()

def find_lords_road(lord:list, G:list[Vertex]):
    V = len(G)

    castles_protected_by_lord = set()
    lord_strength = 0

    visited = [False] * (V+1)

    def DFS(G:list[Vertex], u):
        nonlocal castles_protected_by_lord, lord_strength

        vertex_is_under_lords_protection = False
        visited[u] = True

        for v,w in G[u].out:
            if not visited[v] and DFS(G, v):
                vertex_is_under_lords_protection = True
                lord_strength += w

        if u in lord:
            vertex_is_under_lords_protection = True

        if vertex_is_under_lords_protection: 
            castles_protected_by_lord.add(u)

        return vertex_is_under_lords_protection

    for castle in lord:
        if not visited[castle]:
            castles_protected_by_lord.add(castle)
            DFS(G, castle)

    return lord_strength, castles_protected_by_lord

def lex_BFS(graph: dict[int, Lord], n ,start: int = 1):
    lex_order = []
    S = set()

    verticisSet = set([lord for lord in graph.values()])
    verticisSet.remove(graph[start])

    considered_sets = [verticisSet, {graph[start]}]

    while considered_sets:
        vertex = next(iter(considered_sets[-1]))

        considered_sets[-1].remove(vertex)

        if not considered_sets[-1]:
            considered_sets.pop()

        neighbours = vertex.out

        lex_order.append(vertex.id)
        S.add(vertex.id)

        new_considered_sets = []

        for single_set in considered_sets:
            Y = single_set & neighbours
            X = single_set - Y
            if X:
                new_considered_sets.append(X)

            if Y:
                new_considered_sets.append(Y)

        considered_sets = new_considered_sets

    return lex_order

def get_all_lords(lords:int, kingsroad:list[Vertex], V:int) -> dict[int, Lord]:
    """
    :param lords: list of lists (lords)
    :param kingsroad: graph as adjcacency list, each vertex is Vertex object with out attribute as set of its neighbours
    :param V: numer of lords
    """
    all_lords = {}
    for i in range(V):
        lord = lords[i]
        lord_strength, lord_castles = find_lords_road(lord, kingsroad)
        all_lords[i+1] = Lord(i+1,lord_castles, lord_strength)

    return all_lords

def get_independet_max_weighted_set(graph:dict[int, Lord], V:int) -> set:
    order = lex_BFS(graph, V+1)[::-1]

    RED, BLUE = 0, 1
    weights = {key : value.strength for key, value in graph.items()}
    colors = {key : None for key in graph.keys()}

    for i in range(V):
        lord_i = order[i]
        if weights[lord_i] <= 0:
            weights[lord_i] = 0
            continue

        xi = graph[lord_i]
        colors[lord_i] = RED

        for j in range(i+1,V):
            lord_j = order[j]
            xj = graph[lord_j]

            if xj in xi.out:
                weights[lord_j] -= weights[lord_i]
                if weights[lord_j] < 0: weights[lord_j] = 0
        
        weights[lord_i] = 0
        
    blue_colored_set = set()
    sum_blue = 0

    for i in range(V-1,-1,-1):
        lord_i = order[i]
        xi = graph[lord_i]

        if colors[lord_i] == RED:
            flag = True
            for xj in xi.out:
                if colors[xj.id] == BLUE:
                    flag = False
                    break
            if flag:
                colors[lord_i] = BLUE
                sum_blue += xi.strength
                blue_colored_set.add(lord_i)

    return blue_colored_set, sum_blue

def add_colliding_neighbours_to_lords(all_lords, n):
    vert_map = {}
    for i in range(1, n+1):
        for vert in all_lords[i].castles:
            if vert not in vert_map:
                vert_map[vert] = []
            vert_map[vert].append(all_lords[i])

    for vert, lords in vert_map.items():
        for lord_a in lords:
            for lord_b in lords:
                if lord_a != lord_b:
                    lord_a.out.add(lord_b)
                    lord_b.out.add(lord_a)

def solve(N, streets, lords):
    kingsroad = kruskal((N,streets))
    KR = make_graph(N, kingsroad)
    
    n = len(lords)
    all_lords = get_all_lords(lords, KR, n)

    add_colliding_neighbours_to_lords(all_lords, n)

    _blue_colored_lords_ids, result = get_independet_max_weighted_set(all_lords, n)

    return result

runtests(solve)