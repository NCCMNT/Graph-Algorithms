from queue import PriorityQueue
from tests.tester import run_tests

class Node:
    def __init__(self, vert):
        self.org = vert
        self.active = True
        self.vert = f'{vert}'
        self.edges = {}    # słownik  mapujący wierzchołki do których są krawędzie na ich wagi

    def addEdge( self, v, weight):
        self.edges[v] = self.edges.get(v,0) + weight  # dodaj krawędź do zadanego wierzchołka
                                                        # o zadanej wadze; a jeśli taka krawędź
                                                        # istnieje, to dodaj do niej wagę
    def delEdge( self, to ):
        if to in self.edges:
            del self.edges[to]                             # usuń krawędź do zadanego wierzchołka

    def __repr__(self):
        return f'vert: {self.vert} -> edges:{self.edges}'

def Stoer_Wagner(G1):

    V, L = G1

    G = [ Node(i) for i in range(V) ]

    for (u,v,c) in L:
        u -= 1
        v -= 1
        G[u].addEdge(v,c)
        G[v].addEdge(u,c)

    def mergeVertices(G:list[Node], x, y):
        # y - wierzchołek do usunięcia
        # x - wierzchołek do którego dołączamy y
        if not G[x].active or not G[y].active: return

        for u, weight in G[y].edges.items():
            if u == x: continue
            G[x].addEdge(u, weight)
            G[u].addEdge(x, weight)

        G[x].vert = f'{G[y].vert}{G[x].vert}'
        G[y].active = False

        for u in list(G[y].edges.keys()):
            G[u].delEdge(y)
        G[y].edges.clear()

    def minimumCutPhase( G:list[Node] ):
        active_nodes = [i for i, node in enumerate(G) if node.active]
        start = active_nodes[0]
        weights = {i: 0 for i in active_nodes}
        S = set()
        order = []
        PQ = PriorityQueue()
        PQ.put((-weights[start], start))
        
        while not PQ.empty():
            curren_sum, u = PQ.get()
            curren_sum = -curren_sum

            if u in S: continue

            S.add(u)
            order.append(u)
            
            for v, weight in G[u].edges.items():
                if v not in S and G[v].active:
                    weights[v] += weight
                    PQ.put((-weights[v], v))
        
        s = order[-1]
        t = order[-2]

        # tworzone przecięcie jest postaci S = {s}, T = V - {s}
        cut_result = sum( G[s].edges.values() )

        mergeVertices(G,s,t)

        return cut_result
    
    result = float('inf')
    
    while True:
        cut = minimumCutPhase(G)
        result = min(result, cut)
        ACTIVES = [G[u].active for u in range(V)]
        if ACTIVES.count(True) == 1: break
    return result

run_tests(3, Stoer_Wagner, graph_converter='raw', without='grid100x100')