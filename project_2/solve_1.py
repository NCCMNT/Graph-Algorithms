from data import runtests

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
    
    import sys
    sys.setrecursionlimit(10**6)
    
    holes = set(holes)
    pieces = set(pieces)
    initial_board = Board(frozenset(pieces))
    boards = [initial_board]

    result = False

    def DFS_boards(boards, player : bool):
        nonlocal result
        if result: return result
        
        possible_boards = get_possible_boards(boards[-1])
        possible_boards = list(filter(lambda x: x not in boards, possible_boards))

        if not possible_boards:
            result = not player
            return result
        
        for new_board in possible_boards:
            if result: break

            if new_board not in boards:
                DFS_boards(boards + [new_board], not player)

    DFS_boards(boards, True)
    return result

runtests(my_solve)