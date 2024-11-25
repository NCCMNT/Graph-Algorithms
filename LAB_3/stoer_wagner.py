from dimacs import *

(V,L) = loadWeightedGraph( r'graphs-lab3/simple' ) # wczytaj graf

class Node:
    def __init__(self, vert):
        self.org = vert
        self.deactivated = False
        self.vert = f'{vert}'
        self.edges = {}    # słownik  mapujący wierzchołki do których są krawędzie na ich wagi

    def addEdge( self, to, weight):
        self.edges[to] = self.edges.get(to,0) + weight  # dodaj krawędź do zadanego wierzchołka
                                                        # o zadanej wadze; a jeśli taka krawędź
                                                        # istnieje, to dodaj do niej wagę
    def delEdge( self ):
        self.edges.clear()                             # usuń krawędź do zadanego wierzchołka

    def __repr__(self):
        return f'vert: {self.vert} -> edges:{self.edges}'

def Stoer_Wagner(V,L):

    G = [ Node(i) for i in range(V) ]
    ACTIVE = [not u.deactivated for u in G]

    for (u,v,c) in L:
        u -= 1
        v -= 1
        G[u].addEdge(v,c)
        G[v].addEdge(u,c)

    def mergeVertices(G:list[Node], x, y):
        if G[x].deactivated or G[y].deactivated: return
        G[y].vert = f'{G[x].vert}{G[y].vert}'


        for u, weight in G[x].edges.items():
            if u == y: continue
            G[y].addEdge(u, weight)

        G[x].vert = f'{G[x].org}'
        G[x].delEdge()
        G[x].deactivated = True
        ACTIVE[G[x].org] = False

    def count_weights(v, S):
        count = 0
        for u, weight in G[v].edges.items():
            if u in S:
                count += weight
        return count

    def minimumCutPhase( G:list[Node] ):
        n = len(G)
        S = [0]

        while len(S) != n:
            maxi = 0
            v = None
            for u in range(n):
                current = count_weights(u, S)
                if current > maxi:
                    maxi = current
                    v = u
            if v not in S:
                S.append(v)

        s = S[-1]
        t = S[-2]

        # tworzone przecięcie jest postaci S = {s}, T = V - {s}
        potential_result = count_weights(s, G[s].edges.keys())

        mergeVertices(G,s,t)

        return potential_result
    
    result = float('inf')
    
    x = len(ACTIVE)
    while x != 1:
        cut = minimumCutPhase(G)
        result = min(result, cut)
        x = ACTIVE.count(True)
    return result

print(Stoer_Wagner(V,L))