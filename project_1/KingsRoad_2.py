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

class Lord:
    def __init__(self, id, castles, road, strength):
        self.castles = castles
        self.id = id
        self.road = road
        self.strength = strength
        self.color = None
        self.out = set()

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
        road.update(DFS(lord[i], lord[i+1], G))
    return road

def sum_strength(road):
    return sum(w for _,_,w in road)

def get_vertices(road):
    return {u for u,_,_ in road} | {v for _,v,_ in road}

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
        lord_road = find_lords_road(lord, kingsroad)
        lord_strength = sum_strength(lord_road)
        lord_castles = get_vertices(lord_road)
        all_lords[i+1] = Lord(i+1,lord_castles, lord_road, lord_strength)
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
                blue_colored_set.add(lord_i)

    return blue_colored_set

def add_colliding_neighbours_to_lords(all_lords, n):
    for i in range(1,n+1):
        for j in range(1,n+1):
            if i == j: continue
            edges_a, vertices_a = all_lords[i].road, all_lords[i].castles
            edges_b, vertices_b  = all_lords[j].road, all_lords[j].castles
            if (edges_a & edges_b != set()) or (vertices_a & vertices_b != set()):
                all_lords[i].out.add(all_lords[j])
                all_lords[j].out.add(all_lords[i])

def solve(N, streets, lords):
    kingsroad = kruskal((N,streets))
    KR = make_graph(N, kingsroad)
    
    n = len(lords)
    all_lords = get_all_lords(lords, KR, n)

    add_colliding_neighbours_to_lords(all_lords, n)

    blue_colored_lords_ids = get_independet_max_weighted_set(all_lords, n)

    result = 0
    for lord_i in blue_colored_lords_ids:
        result += all_lords[lord_i].strength
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
runtests(solve)