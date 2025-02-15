from data import runtests
from collections import deque

def max_matching(G : list[list]) -> int:
    """Edmonds blossom algorithm finds max matching in graph G represented as adjecency list"""

    def LCA(matching, blossom_base, parent, u, v):
        n = len(matching)
        visited = [False] * n

        while True:
            # traverse upward through parents until the base of u is found
            u = blossom_base[u]
            visited[u] = True
            if matching[u] == -1:
                break
            u = parent[matching[u]]

        while True:
            # traverse upward until the base of v is found
            v = blossom_base[v]
            if visited[v]:
                return v
            v = parent[matching[v]]

    def mark_blossom_vertices(matching, blossom_base, blossom, parent, v, lca, child):

        while blossom_base[v] != lca:

            # both v and its matching belongs to the blossom
            blossom[blossom_base[v]] = blossom[blossom_base[matching[v]]] = True

            parent[v] = child
            child = matching[v]

            v = parent[matching[v]]

    def find_aumenting_path(G, matching, parent, s):
        n = len(G)

        visited = [False] * n
        visited[s] = True

        parent[:] = [-1] * n
        blossom_base = list(range(n))

        Q = deque([s])

        while Q:

            u = Q.popleft()

            for v in G[u]:

                # ignore if vertices are matched or have the same blossom base
                if blossom_base[u] == blossom_base[v] or matching[u] == v:
                    continue
                
                if v == s or (matching[v] != -1 and parent[matching[v]] != -1):
                    lca = LCA(matching, blossom_base, parent, u, v) # find lowest common ancestor for u and v
                    blossom = [False] * n

                    mark_blossom_vertices(matching, blossom_base, blossom, parent, u, lca, v)
                    mark_blossom_vertices(matching, blossom_base, blossom, parent, v, lca, u)

                    for i in range(n):

                        if blossom[blossom_base[i]]:
                            blossom_base[i] = lca

                            if not visited[i]:
                                visited[i] = True
                                Q.append(i)

                elif parent[v] == -1:
                    # assign BFS parent
                    parent[v] = u

                    if matching[v] == -1:
                        return v
                    
                    v = matching[v]
                    visited[v] = True
                    Q.append(v)
        return -1

    def get_max_matching(G):
        n = len(G)

        matching = [-1] * n
        parent = [None] * n

        for i in range(n):
            if matching[i] == -1:

                v = find_aumenting_path(G, matching, parent, i)
                
                while v != -1:
                    # if augmenting path is found then swap matchings in it
                    parent_v = parent[v]
                    parent_v_match = matching[parent_v]

                    matching[v], matching[parent_v] = parent_v, v

                    v = parent_v_match

        return sum(1 for x in matching if x != -1) // 2

    return get_max_matching(G)

class Board:
    def __init__(self, pieces_position : frozenset[tuple [str, int, int]], id : int):
        self.pieces_positions = pieces_position
        self.out = set()
        self.id = id
    
    def __eq__(self, other):
        return self.pieces_positions == other.pieces_positions
    
    def __hash__(self):
        return hash(self.pieces_positions)

def my_solve(N, M, holes, pieces):

    directions = {
        "k": [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)],
        "n": [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)],
        "r": [(0, 1), (0, -1), (1, 0), (-1, 0)],
        "b": [(1, 1), (1, -1), (-1, 1), (-1, -1)]
    }

    def get_move_set(piece, x, y, other_pieces):
        move_set = []
        
        if piece in directions:
            for dx, dy in directions[piece]:
                nx, ny = x + dx, y + dy
                while 1 <= nx <= N and 1 <= ny <= M and (nx, ny) not in holes:
                    if (nx, ny) not in other_pieces:
                        move_set.append((nx, ny))
                    if piece in "kn":  
                        break
                    nx += dx
                    ny += dy
        elif piece == "q":
            move_set.extend(get_move_set("r", x, y, other_pieces))
            move_set.extend(get_move_set("b", x, y, other_pieces))
        
        return move_set
    
    def get_possible_boards(board : Board, visited : set[Board], G) -> set[Board]:
        nonlocal id
        possible_boards = set()
        other_pices = set((x,y) for _, x, y in board.pieces_positions)

        for piece, x, y in board.pieces_positions:
            move_set = get_move_set(piece, x, y, other_pices)

            for nx, ny in move_set:
                new_pieces_positions = board.pieces_positions - {(piece, x, y)} | {(piece, nx, ny)}

                if new_pieces_positions not in visited:
                    new_board = Board(frozenset(new_pieces_positions), id)
                    id += 1
                    possible_boards.add(new_board)
                else:
                    possible_boards.add(G[new_pieces_positions])
                visited.add(new_pieces_positions)
        
        return possible_boards

    def make_graph(init_b : Board):
        E = set()
        G = {init_b.pieces_positions : init_b}
        visited = set()
        visited_pos = set()
        Q = deque([init_b])

        while Q:
            considered_board = Q.popleft()

            if considered_board in visited:
                continue

            visited.add(considered_board)

            neighbours = get_possible_boards(considered_board, visited_pos, G)

            for neighbour in neighbours:
                if neighbour.pieces_positions not in G:
                    G[neighbour.pieces_positions] = neighbour

                E.add((considered_board.id, G[neighbour.pieces_positions].id))

                # if neighbour not in visited:
                Q.append(neighbour)
        
        return E
    
    def edges_to_graph(edges):
        n = max(max(edges, default=(0, 0))) + 1

        G = [[] for _ in range(n)]
        G2 = [[] for _ in range(n)]

        for u,v in edges:
            G[u].append(v)

            if u != 0 and v != 0:
                G2[u].append(v)

        return G, G2

    holes = set(holes)
    pieces = set(pieces)
    id = 0
    initial_board = Board(frozenset(pieces), id)
    id += 1

    E = make_graph(initial_board)

    G, G2 = edges_to_graph(E)

    mm = max_matching(G)
    mm2 = max_matching(G2)

    return  mm != mm2

runtests(my_solve)