from data import runtests
import sys
sys.setrecursionlimit(10**6)

class Board:
    def __init__(self, pieces_position : frozenset[tuple [str, int, int]]):
        self.pieces_positions = pieces_position
        self.is_winning = None
        self.out = set()
    
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
                    move_set.append((nx, ny))
                    if piece in "kn":
                        break
                    nx += dx
                    ny += dy
        elif piece == "q":
            move_set.extend(get_move_set("r", x, y, other_pieces))
            move_set.extend(get_move_set("b", x, y, other_pieces))
        
        return [pos for pos in move_set if pos not in other_pieces]
    
    def get_possible_boards(board : Board) -> set[Board]:
        possible_boards = set()
        other_pices = set((x,y) for _, x, y in board.pieces_positions)

        for piece, x, y in board.pieces_positions:
            move_set = get_move_set(piece, x, y, other_pices)

            for nx, ny in move_set:
                new_pieces_positions = set(board.pieces_positions)
                new_pieces_positions.remove((piece, x, y))
                new_pieces_positions.add((piece, nx, ny))
                possible_boards.add(Board(frozenset(new_pieces_positions)))
        
        return possible_boards
    
    holes = set(holes)
    pieces = set(pieces)
    initial_board = Board(frozenset(pieces))

    def mex(values):
        values = sorted(set(values))
        for i, v in enumerate(values):
            if i != v:
                return i
        return len(values)

    holes = set(holes)
    pieces = frozenset(pieces)
    initial_board = Board(pieces)
    
    grundy = {}

    def compute_grundy(board: Board):
        if board in grundy:
            return grundy[board]

        possible_boards = get_possible_boards(board)

        if not possible_boards:
            grundy[board] = 0
            return 0

        grundy_values = [compute_grundy(new_board) for new_board in possible_boards]
        grundy[board] = mex(grundy_values)

        return grundy[board]

    return compute_grundy(initial_board) != 0

runtests(my_solve)