from collections import deque
from tests.tester import run_tests

def DFS(G, parent, s ,t):
    n = len(G)
    visited = [False for _ in range(n)]
    visited[s] = True

    def DFSvisit(G,parent,u):
        nonlocal visited, t

        if u == t: return True

        visited[u] = True
        for v, cost in G[u]:
            if not visited[v] and cost != 0:
                visited[v] = True
                parent[v] = u
                DFSvisit(G,parent,v)

    for u in range(n):
        if not visited[u]:
            if DFSvisit(G,parent,u): return True
    return False

def BFS(G, parent, s, t):
    n = len(G)
    Q = deque()
    Q.append(s)
    visited = [False for _ in range(n)]
    visited[s] = True
    
    while Q:
        u = Q.popleft()

        for v, cost in G[u]:
            if not visited[v] and cost != 0:
                visited[v] = True
                parent[v] = u
                Q.append(v)
                if v == t: return True
    return False

def getCost(G,s,t):
    for v, cost in G[s]:
        if v == t: return cost

def checkConnection(G,s,t):
    for v, cost in G[s]:
        if v == t: return True
    return False

def residualPath(G, parent, v):
    bottle_neck = float('inf')
    tmp = v

    while parent[v] is not None:
        bottle_neck = min(bottle_neck, getCost(G,parent[v], v))
        v = parent[v]
    
    v = tmp

    while parent[v] is not None:
        cost_forward = getCost(G, parent[v], v)

        G[parent[v]].remove((v,cost_forward))
        G[parent[v]].append((v,cost_forward - bottle_neck))

        if checkConnection(G, v, parent[v]):
            cost_backward = getCost(G, v, parent[v])
            G[v].remove((parent[v], cost_backward))
            G[v].append((parent[v], cost_backward + bottle_neck))
        else:
            G[v].append((parent[v], bottle_neck))

        v = parent[v]

    return bottle_neck

def fordFulkerson(G, s, t, traversal):
    n = len(G)
    max_flow = 0
    parent = [None for _ in range(n)]

    while traversal(G, parent, s, t):
        max_flow += residualPath(G,parent,t)

    return max_flow

def printSolution(G, s = 0, t = 1, traversal = BFS):
    t = len(G) - 1
    return fordFulkerson(G,s,t, traversal)


run_tests(2, printSolution, subdir='flow', directed=True, graph_converter='dirlist')