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

def LexBFS(G:list[Node], start:int = 1):
	n = len(G)
	lex_order = []
	S = set(range(1,n))
	S.remove(start)

	considered_sets = [S, {start}]

	while considered_sets:
		vertex = next(iter(considered_sets[-1]))
		considered_sets[-1].remove(vertex)
        
		if not considered_sets[-1]: considered_sets.pop()
        
		neighbours = G[vertex].out
		lex_order.append(vertex)
        
		new_considered_sets = []
        
		for single_set in considered_sets:
			Y = single_set.intersection(neighbours)
			K = single_set - Y
			if K: new_considered_sets.append(K)
			if Y: new_considered_sets.append(Y)
            
		considered_sets = new_considered_sets

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