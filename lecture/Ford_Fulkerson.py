# Maksymalny przepływ
# Wejście:
#   G = (V,E) - graf skierowany
#   s,t należące do V
#   c: V x V -> N - funkcja pojemności dla każdej pary wierzchołków
#   jesli (u,v) nie należy do E to c(u,v) = 0, c(u,u) = 0
#
# Przepływ to funkcja f: V x V -> N, taka że: (dla każdego u,v należącego do V f(u,v) <= c(u,v))
# Dla każego v należącego do V\{s,t} [suma po każdym u należącym do V z f(u,v)] = [suma po każdym u należącym do V z f(v,u)]
# Wartość przepływu |f| = [suma po v należących do V z f(s,v)] - [suma po v należących do V z f(v,s)]
#
# Zadanie: Znaleźć przepływ o maksymalnej wartości

from collections import deque
from copy import deepcopy
from math import inf

def BFS(G,parent,s,t):
    n = len(G)
    visited = [False] * n
    visited[s] = True
    queue = deque()
    queue.append(s)

    while queue:
        u = queue.popleft()
        for v in range(n):
            if not visited[v] and G[u][v] > 0:
                visited[v] = True
                parent[v] = u
                queue.append(v)
                if v == t: return True
    return False

def augmentThePath(G,parent,v):
    bottleneck = inf
    tmp = v

    while parent[v] != None:
        bottleneck = min(bottleneck, G[parent[v]][v])
        v = parent[v]
    
    v = tmp

    while parent[v] != None:
        G[parent[v]][v] -= bottleneck 
        G[v][parent[v]] += bottleneck 
        v = parent[v]
    
    return bottleneck 

def Ford_Fulkerson(M, s, t): # M - graf reprezentowany w postaci macierzowej, s - zrodlo, t - ujscie
    n = len(M)
    G = deepcopy(M)

    parent  = [None] * n
    maxFlow = 0

    while BFS(G, parent, s, t):
        bottleNeck = augmentThePath(G, parent, t)
        maxFlow += bottleNeck 

    return maxFlow

G = [[0, 16, 13, 0, 0, 0],
        [0, 0, 10, 12, 0, 0],
        [0, 4, 0, 0, 14, 0],
        [0, 0, 9, 0, 0, 20],
        [0, 0, 0, 7, 0, 4],
        [0, 0, 0, 0, 0, 0] ]

print( Ford_Fulkerson(G, 0, 5) ) # 23