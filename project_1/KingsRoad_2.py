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

class Lord_Node:
  def __init__(self, idx, strength):
    self.idx = idx
    self.strength = strength
    self.out = set()
    self.color = None

  def connect_to(self, v):
    self.out.add(v)

def make_graph_of_lords(V, L:dict[int, set], lords_roads):
    G = [None] + [Lord_Node(i, lords_roads[i].strength) for i in range(1, V+1)]

    for lord_num, lord_neighbours in L.items():
        G[lord_num].out = lord_neighbours

    return G

def LexBFS(G,n):
    # n = len(G)
    lex_order = []
    S = [set()]

    for u in range(1,n):
        S[0].add(u)
    
    def divide_sets(S:list[set], vertex:Lord, G:list[Lord]):
        n = len(S)
        
        for i in range(n):
            current_set = S[i]
            
            N = G[vertex].out

            X = current_set.difference(N)
            Y = current_set.intersection(N)
            
            if bool(X) and bool(Y):
                S[i] = X
                S.insert(i+1, Y)
            elif bool(X) and (not bool(Y)): S[i] = X
            elif (not bool(X)) and bool(Y): S[i] = Y
    
    while S:
        u = S[-1].pop()
        lex_order.append(u)
        divide_sets(S, u, G)
        if not bool(S[-1]): S.pop()
    
    return lex_order

class Lord:
    def __init__(self, id, castles, road, strength):
        self.castles = castles
        self.id = id
        self.road = road
        self.strength = strength
        self.color = None
        self.out = set()

# sys.setrecursionlimit(10_000)

class POECheck:
    def __init__(self, lexOrder: list, graph: dict[int, Lord]):
        self.lexOrder = lexOrder
        self.lexSmallerNeighbors = {graph[lexOrder[0]] : set()}
        self.parents = {graph[lexOrder[0]] : graph[lexOrder[0]]}

        visitedSet = {graph[lexOrder[0]]}

        n = len(lexOrder)

        for idx in range(1, n):
            vertex = graph[lexOrder[idx]]

            self.lexSmallerNeighbors[vertex] = visitedSet & vertex.out

            visitedSet.add(vertex)

def solve(N, streets, lords):
    G = (N,streets)
    kingsroad = kruskal(G)
    KR = make_graph(N, kingsroad)
    
    n = len(lords)
    all_lords = {}
    for i in range(n):
        lord = lords[i]
        lord_road = find_lords_road(lord,KR)
        lord_strength = sum_strength(lord_road)
        lord_castles = get_vertices(lord_road)
        all_lords[i+1] = Lord(i+1,lord_castles, lord_road, lord_strength)

    for i in range(1,n+1):
        for j in range(1,n+1):
            if i == j: continue
            edges_a, vertices_a = all_lords[i].road, all_lords[i].castles
            edges_b, vertices_b  = all_lords[j].road, all_lords[j].castles
            if (edges_a & edges_b != set()) or (vertices_a & vertices_b != set()):
                all_lords[i].out.add(all_lords[j])
                all_lords[j].out.add(all_lords[i])

    order = LexBFS(all_lords, n+1)[::-1]

    RED, BLUE = 0, 1
    weights = {key : value.strength for key, value in all_lords.items()}

    # poe = POECheck(order, all_lords)

    for i in range(n):
        lord_i = order[i]
        if weights[lord_i] <= 0:
            weights[lord_i] = 0
            continue

        xi = all_lords[lord_i]
        xi.color = RED

        for j in range(i+1,n): # poe.lexSmallerNeighbors[xi]:
            lord_j = order[j]
            xj = all_lords[lord_j] #lord_j = xj.id

            if xj in xi.out:
                weights[lord_j] -= weights[lord_i]
                if weights[lord_j] < 0: weights[lord_j] = 0
        
        weights[lord_i] = 0
            
    blue_colored_lords = set()

    for i in range(n-1,-1,-1):

        xi = all_lords[order[i]]

        if xi.color == RED:
            flag = True
            for xj in xi.out:
                if xj.color == BLUE:
                    flag = False
                    break
            if flag:
                xi.color = BLUE
                blue_colored_lords.add(xi)

    result = 0
    for lord in blue_colored_lords:
        result += lord.strength
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