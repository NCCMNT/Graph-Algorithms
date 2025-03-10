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

    # def get_move_set(piece, x, y, other_pices):

    #     move_set = []

    #     match piece:
            
    #         # get legal moves for king piece keeping board bounds and not entering holes
    #         case "k":
    #             moves = [(x, y + 1), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1)]
    #             for x, y in moves:
    #                 if (0 < x <= N) and (0 < y <= M) and ((x,y) not in holes) and ((x,y) not in other_pices):
    #                     move_set.append((x,y))

    #         # get legal moves for knight piece keeping board bounds and not entering holes
    #         case "n":
    #             moves = [(x - 1, y + 2), (x + 1, y + 2), (x + 2, y + 1), (x + 2, y - 1), (x + 1, y - 2), (x - 1, y - 2), (x - 2, y - 1), (x - 2, y+ 1)]
    #             for x, y in moves:
    #                 if (0 < x <= N) and (0 < y <= M) and ((x,y) not in holes) and ((x,y) not in other_pices):
    #                     move_set.append((x,y))
            
    #         # get legal moves for rook piece keeping board bound and stopping upon approaching a hole
    #         case "r":
    #             NORTH = EAST = SOUTH = WEST = True
    #             for i in range(1, max(N,M) + 1):

    #                 if NORTH:
    #                     if (0 < y + i <= M) and ((x, y + i) not in holes) and ((x, y + i) not in other_pices):
    #                         move_set.append((x, y + i))
    #                     else:
    #                         NORTH = False
    #                 if EAST:
    #                     if (0 < x + i <= N) and ((x + i, y) not in holes) and ((x + i, y) not in other_pices):
    #                         move_set.append((x + i, y))
    #                     else:
    #                         EAST = False

    #                 if SOUTH:
    #                     if (0 < y - i <= M) and ((x , y - i) not in holes) and ((x , y - i) not in other_pices):
    #                         move_set.append((x, y - i))
    #                     else:
    #                         SOUTH = False

    #                 if WEST:
    #                     if (0 < x - i <= N) and ((x - i, y) not in holes) and ((x - i, y) not in other_pices):
    #                         move_set.append((x - i, y))
    #                     else:
    #                         WEST = False
            
    #         # get legal moves for bishop piece keeping board bound and stopping upon approaching a hole
    #         case "b":
    #             BR = BL = TR = TL = True
    #             for i in range(1, max(N,M) + 1):
    #                 if not BR and not BL and not TR and not TL: break
                    
    #                 # reaching for top right corner
    #                 if TR:
    #                     if (0 < x + i <= N) and (0 < y + i <= M) and ((x + i, y + i) not in holes) and ((x + i, y + i) not in other_pices):
    #                         move_set.append((x + i, y + i))
    #                     else:
    #                         TR = False

    #                 # reaching for top left corner
    #                 if TL:
    #                     if (0 < x - i <= N) and (0 < y + i <= M) and ((x - i, y + i) not in holes) and ((x - i, y + i) not in other_pices):
    #                         move_set.append((x - i, y + i))
    #                     else:
    #                         TL = False
                    
    #                 # reaching for bottom left corner
    #                 if BL:
    #                     if (0 < x - i <= N) and (0 < y - i <= M) and ((x - i, y - i) not in holes) and ((x - i, y - i) not in other_pices):
    #                         move_set.append((x - i, y - i))
    #                     else:
    #                         BL = False
                    
    #                 # reaching fot bottom right corner
    #                 if BR:
    #                     if (0 < x + i <= N) and (0 < y - i <= M) and ((x + i, y - i) not in holes) and ((x + i, y - i) not in other_pices):
    #                         move_set.append((x + i, y - i))
    #                     else:
    #                         BR = False

    #         # get legal moves for queen piece that combine all legal moves from rook and bishop moveset
    #         case "q": move_set = get_move_set("r", x, y, other_pices) + get_move_set("b", x, y, other_pices)
        
    #     return move_set
    
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
    
    b = set()
    b.add(initial_board)

    return DFS(initial_board, b)

    # boards = [initial_board]
    # boards_after_first_move = get_possible_boards(initial_board)
    # boards_after_first_move = list(filter(lambda x: x not in boards, boards_after_first_move))

    # result = False

    # def DFS_boards(boards, player : bool):
    #     nonlocal result
    #     if result: return result
        
    #     possible_boards = get_possible_boards(boards[-1])
    #     possible_boards = list(filter(lambda x: x not in boards, possible_boards))

    #     if not possible_boards:
    #         result = not player
    #         return result
        
    #     for new_board in possible_boards:
    #         if result: break

    #         if new_board not in boards:
    #             DFS_boards(boards + [new_board], not player)

    # DFS_boards(boards, True)
    # return result

    

    # def DFS_boards(boards : list[Board]):
        
    #     possible_boards = get_possible_boards(boards[-1])
    #     possible_boards = list(filter(lambda x: x not in boards, possible_boards))

    #     if not possible_boards:
    #         boards[-1].is_winning = False
    #         return
        
    #     for new_board in possible_boards:

    #         if new_board not in boards:

    #             DFS_boards(boards + [new_board])

    #             boards[-1].is_winning = (not new_board.is_winning)


    # DFS_boards(boards)
    # return initial_board.is_winning

    


runtests(my_solve)

print(my_solve(1, 3,
  [],
  [("k", 1, 2)]))

# print(my_solve(2, 5,
#   [(2, 1), (2, 3), (2, 4), (2, 5)],
#   [("k", 2, 2)]))

# print(my_solve(3, 3,
#   [(2, 1), (2, 2), (2, 3)],
#   [("k", 1, 2), ("q", 3, 3)],
#   ))
