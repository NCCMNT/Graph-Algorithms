
class Node:
  def __init__(self, idx):
    self.idx = idx
    self.out = set()

  def connect_to(self, v):
    self.out.add(v)
    
def make_graph(V,L):
	G = [None] + [Node(i) for i in range(1, V+1)]

	for (u, v, _) in L:
		G[u].connect_to(v)
		G[v].connect_to(u)
    
	return G

def LexBFS(G):
    n = len(G)
    lex_order = []
    S = [set()]

    for u in range(1,n):
        S[0].add(u)
    
    def divide_sets(S:list[set], vertex:Node, G:list[Node]):
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
            
def checkLexBFS(G, vs):
  n = len(G)
  pi = [None] * n
  for i, v in enumerate(vs):
    pi[v] = i

  for i in range(n-1):
    for j in range(i+1, n-1):
      Ni = G[vs[i]].out
      Nj = G[vs[j]].out

      verts = [pi[v] for v in Nj - Ni if pi[v] < i]
      if verts:
        viable = [pi[v] for v in Ni - Nj]
        if not viable or min(verts) <= min(viable):
          return False
  return True