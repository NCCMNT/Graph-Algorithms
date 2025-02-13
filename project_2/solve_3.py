from data import runtests

class Board:
    def __init__(self, pieces_position : frozenset[tuple [str, int, int]]):
        self.pieces_positions = pieces_position
        self.out = set()
    
    def __eq__(self, other):
        return self.pieces_positions == other.pieces_positions
    
    def __hash__(self):
        return hash(self.pieces_positions)

def my_solve(N, M, holes, pieces):

    def get_move_set(piece, x, y, other_pieces):
        move_set = []
        directions = {
            "k": [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)],
            "n": [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)],
            "r": [(0, 1), (0, -1), (1, 0), (-1, 0)],
            "b": [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        }
        
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
        possible_boards = set()
        other_pices = set((x,y) for _, x, y in board.pieces_positions)

        for piece, x, y in board.pieces_positions:
            move_set = get_move_set(piece, x, y, other_pices)

            for nx, ny in move_set:
                new_pieces_positions = board.pieces_positions - {(piece, x, y)} | {(piece, nx, ny)}
                # new_pieces_positions = set(board.pieces_positions)
                # new_pieces_positions.remove((piece, x, y))
                # new_pieces_positions.add((piece, nx, ny))
                new_board = Board(frozenset(new_pieces_positions))
                possible_boards.add(new_board)
        
        return possible_boards
    
    from collections import deque

    def make_graph(init_b):
        G = {}
        visited = set()

        Q = deque([init_b])
        G[init_b.pieces_positions] = init_b

        while Q:
            considered_board = Q.popleft()

            if considered_board in visited:
                continue

            visited.add(considered_board)

            neighbours = get_possible_boards(considered_board)
            considered_board.out = set()

            for neighbour in neighbours:
                if neighbour.pieces_positions in G:
                    neighbour = G[neighbour.pieces_positions]
                else:
                    G[neighbour.pieces_positions] = neighbour

                considered_board.out.add(neighbour)
                Q.append(neighbour)
        
        return G
    
    def find_longest_path(s):

        def dfs(node, visited):
            if node in visited:
                return 0

            visited.add(node)
            max_length = 0

            for neighbor in node.out:
                max_length = max(max_length, 1 + dfs(neighbor, visited))

            visited.remove(node)
            return max_length
        
        longest_path = dfs(s, set())
        return longest_path
    
    holes = set(holes)
    pieces = set(pieces)
    initial_board = Board(frozenset(pieces))
    G = make_graph(initial_board)
    # print(G)
    return max((find_longest_path(initial_board) - 1), 0) % 2 == 1

# print(my_solve(2, 5,
#   [(2, 1), (2, 3), (2, 4), (2, 5)],
#   [("k", 2, 2)]))

runtests(my_solve)