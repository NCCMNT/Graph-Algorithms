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

    result = 0
    max_mask = 2**n
    for mask in range(1,max_mask):
        i = 0
        considered_set = set()
        potential_result = 0
        while i < n:
            _, cuurent_strength, current_set = all_lords_roads[i]
            if mask % 2 == 1:
                if considered_set & current_set == set():
                    considered_set |= current_set
                    potential_result += cuurent_strength
                else: break
            mask //= 2
            i += 1
        result = max(result, potential_result)

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

# A = solve(4, [
#   (1, 2, 2),
#   (2, 3, 3),
#   (2, 4, 5),
#   ],
#   [
#     [1, 3, 4],
#   ])

# A = solve(5, [
#   (1, 2, 3),
#   (2, 3, 5),
#   (2, 4, 4),
#   (2, 5, 6),
#   (1, 4, 8),
#   (4, 3, 9),
#   (5, 3, 11),
#   (1, 5, 13),
#   ],
#   [
#     [1, 3],
#     [4, 5],
#   ])
# print(A)
runtests(solve)