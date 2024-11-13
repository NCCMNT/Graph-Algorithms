from dimacs import *

(V,L) = loadWeightedGraph( r'graphs-lab3/trivial' ) # wczytaj graf

class Node:
    def __init__(self):
        self.edges = {}    # słownik  mapujący wierzchołki do których są krawędzie na ich wagi

    def addEdge( self, to, weight):
        self.edges[to] = self.edges.get(to,0) + weight  # dodaj krawędź do zadanego wierzchołka
                                                        # o zadanej wadze; a jeśli taka krawędź
                                                        # istnieje, to dodaj do niej wagę
    def delEdge( self, to ):
        del self.edges[to]                              # usuń krawędź do zadanego wierzchołka

    def __repr__(self):
        return f'{self.edges}'

G = [ Node() for _ in range(V) ]

for (u,v,c) in L:
    u -= 1
    v -= 1
    G[u].addEdge(v,c)
    G[v].addEdge(u,c)

for i in range(len(G)):
    print(i, G[i])

def mergeVertices(G:list[Node], u, v):
    merged_vert = f'{u}-{v}'
    if v in G[u].edges.keys(): G[u].delEdge(v)

    for edge, weight in G[v].edges.items():
        G[u].addEdge(edge, weight)
        G[v].delEdge(edge)
    
    return merged_vert