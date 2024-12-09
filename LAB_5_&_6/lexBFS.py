
class Node:
  def __init__(self, idx):
    self.idx = idx
    self.out = set()

  def connect_to(self, v):
    self.out.add(v)

V = 8
L = [
   (1,6,0),
   (6,3,0),
   (6,8,0),
   (6,7,0),
   (3,8,0),
   (8,2,0),
   (8,5,0),
   (8,4,0),
   (8,7,0),
   (7,5,0),
   (7,4,0),
]

# G = [None] + [Node(i) for i in range(1, V+1)]

# for (u, v, _) in L:
#   G[u].connect_to(v)
#   G[v].connect_to(u)

# for i in range(V+1):
#    if i == 0: continue
#    print(G[i].out)

G = [[] for _ in range(V+1)]

for (u,v,_) in L:
   G[u].append(v)
   G[v].append(u)


def LexBFS(G):
    n = len(G)
    lex_order = []
    S = [set()]

    for u in range(n):
        S[0].add(u)
    
    
    def divide_sets(S:list[set], vertex, G):
        n = len(S)
        neighbours = set()
        for u in G[vertex]:
            neighbours.add(u)
        
        for i in range(n):
            current_set = S[i]
            N = set()

            for element in current_set:
                if element in neighbours:
                    N.add(element)

            X = current_set.difference(N)
            Y = current_set.intersection(N)

            if bool(X) and bool(Y):
                S[i] = X
                S.insert(i+1, Y)
            elif bool(X) and not bool(Y): S[i] = X
            elif not bool(X) and bool(Y): S[i] = Y
            else: S.pop(i)

            print(S)
    
    while S:
        u = S[-1].pop()
        lex_order.append(u)
        # print(lex_order)
        # print(S)
        divide_sets(S, u, G)
    
    return lex_order

print(LexBFS(G))

            
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
        
