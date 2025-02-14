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
    
    holes = set(holes)
    pieces = set(pieces)
    initial_board = Board(frozenset(pieces))

    def DFS(board: Board, banned : set):
        possible_boards = get_possible_boards(board)
        possible_boards = [b for b in possible_boards if b not in banned]

        if not possible_boards:
            board.is_winning = False
            return False
        
        board.out.update(possible_boards)

        for new_board in possible_boards:

            if new_board not in banned:
                banned.add(new_board)
                DFS(new_board, banned)
                banned.remove(new_board)

        if any(not n.is_winning for n in board.out):
            board.is_winning = True
        else:
            board.is_winning = False

        return board.is_winning
    
    # from collections import deque

    # def BFS(board: Board):
    #     Q = deque()
    #     Q.append((board, set([board])))
    #     visited = set()
    #     visited.add(board)
        
    #     while Q:
    #         current_board, banned = Q.popleft()
    #         possible_boards = get_possible_boards(current_board)
    #         possible_boards = [b for b in possible_boards if b not in banned]
            
    #         if not possible_boards:
    #             current_board.is_winning = False
    #             continue
            
    #         current_board.out.update(possible_boards)

    #         for new_board in possible_boards:
    #             if new_board not in visited:
    #                 visited.add(new_board)
    #                 new_banned = banned.copy()  # Create a COPY of the banned set
    #                 new_banned.add(new_board)
    #                 Q.append((new_board, new_banned))
            
    #         if any(not n.is_winning for n in current_board.out):
    #             current_board.is_winning = True
    #         else:
    #             current_board.is_winning = False
        
    #     return board.is_winning

    b = set()
    b.add(initial_board)

    # return BFS(initial_board)
    return DFS(initial_board, b)


runtests(my_solve)