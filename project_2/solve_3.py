from data import runtests
from collections import deque

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
    
    def get_possible_boards(board : Board) -> set[Board]:
        nonlocal id
        possible_boards = set()
        other_pices = set((x,y) for _, x, y in board.pieces_positions)

        for piece, x, y in board.pieces_positions:
            move_set = get_move_set(piece, x, y, other_pices)

            for nx, ny in move_set:
                new_pieces_positions = board.pieces_positions - {(piece, x, y)} | {(piece, nx, ny)}
                new_board = Board(frozenset(new_pieces_positions), id)
                id += 1
                possible_boards.add(new_board)
        
        return possible_boards

    def make_graph(init_b : Board):
        E = set()
        G = {init_b.pieces_positions : init_b}
        visited = set()
        Q = deque([init_b])

        while Q:
            considered_board = Q.popleft()

            if considered_board in visited:
                continue

            visited.add(considered_board)

            neighbours = get_possible_boards(considered_board)

            for neighbour in neighbours:
                if neighbour.pieces_positions not in G:
                    G[neighbour.pieces_positions] = neighbour

                E.add((considered_board.id, G[neighbour.pieces_positions].id))

                # considered_board.out.add(neighbour)
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

    def lca(match, base, p, a, b):
        used = [False] * len(match)
        while True:
            a = base[a]
            used[a] = True
            if match[a] == -1:
                break
            a = p[match[a]]
        while True:
            b = base[b]
            if used[b]:
                return b
            b = p[match[b]]

    # Mark the path from v to the base of the blossom
    def mark_path(match, base, blossom, p, v, b, children):
        while base[v] != b:
            blossom[base[v]] = blossom[base[match[v]]] = True
            p[v] = children
            children = match[v]
            v = p[match[v]]

    def find_path(graph, match, p, root):
        n = len(graph)
        used = [False] * n
        p[:] = [-1] * n
        base = list(range(n))
        used[root] = True
        Q = deque([root])

        while Q:
            v = Q.popleft()
            for to in graph[v]:
                if base[v] == base[to] or match[v] == to:
                    continue
                if to == root or (match[to] != -1 and p[match[to]] != -1):
                    curbase = lca(match, base, p, v, to)
                    blossom = [False] * n
                    mark_path(match, base, blossom, p, v, curbase, to)
                    mark_path(match, base, blossom, p, to, curbase, v)
                    for i in range(n):
                        if blossom[base[i]]:
                            base[i] = curbase
                            if not used[i]:
                                used[i] = True
                                Q.append(i)
                elif p[to] == -1:
                    p[to] = v
                    if match[to] == -1:
                        return to
                    to = match[to]
                    used[to] = True
                    Q.append(to)
        return -1

    # Implementation of Blossom Algorithm
    def max_matching(graph):
        n = len(graph)
        match = [-1] * n
        p = [0] * n
        for i in range(n):
            if match[i] == -1:
                v = find_path(graph, match, p, i)
                while v != -1:
                    pv = p[v]
                    ppv = match[pv]
                    match[v] = pv
                    match[pv] = v
                    v = ppv
        # Returns number of pairs in graph
        return sum(1 for x in match if x != -1) // 2


    # holes = set(holes)
    # pieces = set(pieces)
    id = 0
    initial_board = Board(frozenset(pieces), id)
    id += 1

    E = make_graph(initial_board)

    G, G2 = edges_to_graph(E)

    mm = max_matching(G)
    mm2 = max_matching(G2)
    print(mm)
    print(mm2)

    return  mm != mm2

runtests(my_solve)