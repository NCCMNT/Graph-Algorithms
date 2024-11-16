from queue import PriorityQueue
from tests.tester import run_tests

INF = float('inf')

def Dijkstra(G, start = 0):
    n = len(G)
    distances = [-INF for _ in range(n)]
    distances[start] = 0
    visited = [False for _ in range(n)]
    parent = [None for _ in range(n)]
    PQ = PriorityQueue()
    PQ.put((0,start))

    while not PQ.empty():
        _w, u = PQ.get()

        if visited[u]: continue
        visited[u] = True

        for v, cost in G[u]:
            if not visited[v] and distances[v] < cost:
                parent[v] = u
                distances[v] = cost
                PQ.put((-cost,v))

    parent[0] = None
    return parent, distances

def getSolution(G,start = 0):
    parent, distances = Dijkstra(G,start)
    par = parent[1]
    res = distances[1]
    while par != 0:
        res = min(res,distances[par])
        par = parent[par]
    return res

run_tests(1, getSolution)