from data import runtests

class Board:
    def __init__(self, id : int, pieces_position : list[tuple [str, int, int]]):
        self.id = id
        self.pieces_positions = pieces_position
    
    def __eq__(self, other):
        return self.pieces_positions == other.pieces_positions
    
    def __hash__(self):
        return hash(self.id)

def my_solve(N, M, holes, pieces):

    def get_move_set(piece, x, y):

        move_set = []

        match piece:
            
            # get legal moves for king piece keeping board bounds and not entering holes
            case "k":
                moves = [(x, y + 1), (x + 1, y + 1), (x + 1, y), (x + 1, y - 1), (x, y - 1), (x - 1, y - 1), (x - 1, y), (x - 1, y + 1)]
                for x, y in moves:
                    if (0 < x <= N) and (0 < y <= M) and (x,y) not in holes:
                        move_set.append((x,y))

            # get legal moves for knight piece keeping board bounds and not entering holes
            case "n":
                moves = [(x - 1, y + 2), (x + 1, y + 2), (x + 2, y + 1), (x + 2, y - 1), (x + 1, y - 2), (x - 1, y - 2), (x - 2, y - 1), (x - 2, y+ 1)]
                for x, y in moves:
                    if (0 < x <= N) and (0 < y <= M) and (x,y) not in holes:
                        move_set.append((x,y))
            
            # get legal moves for rook piece keeping board bound and stopping upon approaching a hole
            case "r":
                NORTH = EAST = SOUTH = WEST = True
                for i in range(1, max(N,M) + 1):

                    if NORTH:
                        if (0 < y + i <= M) and (x, y + i) not in holes:
                            move_set.append((x, y + i))
                        else:
                            NORTH = False
                            continue
                    if EAST:
                        if (0 < x + i <= N) and (x + i, y) not in holes:
                            move_set.append((x + i, y))
                        else:
                            EAST = False
                            continue

                    if SOUTH:
                        if (0 < y - i <= M) and (x , y - i) not in holes:
                            move_set.append((x, y - i))
                        else:
                            SOUTH = False
                            continue

                    if WEST:
                        if (0 < x - i <= N) and (x - i, y) not in holes:
                            move_set.append((x - i, y))
                        else:
                            WEST = False
                            continue
            
            # get legal moves for bishop piece keeping board bound and stopping upon approaching a hole
            case "b":
                BR = BL = TR = TL = True
                for i in range(1, max(N,M) + 1):
                    
                    # reaching for top right corner
                    if TR:
                        if (0 < x + i <= N) and (0 < y + i <= M) and (x + i, y + i) not in holes:
                            move_set.append((x + i, y + i))
                        else:
                            TR = False
                            continue

                    # reaching for top left corner
                    if TL:
                        if (0 < x - i <= N) and (0 < y + i <= M) and (x - i, y + i) not in holes:
                            move_set.append((x - i, y + i))
                        else:
                            TL = False
                            continue
                    
                    # reaching for bottom left corner
                    if BL:
                        if (0 < x - i <= N) and (0 < y - i <= M) and (x - i, y - i) not in holes:
                            move_set.append((x - i, y - i))
                        else:
                            BL = False
                            continue
                    
                    # reaching fot bottom right corner
                    if BR:
                        if (0 < x + i <= N) and (0 < y - i <= M) and (x + i, y - i) not in holes:
                            move_set.append((x + i, y - i))
                        else:
                            BR = False
                            continue

            # get legal moves for queen piece that combine all legal moves from rook and bishop moveset
            case "q": move_set = get_move_set("r", x, y) + get_move_set("b", x, y)
        
        return move_set
    
    def get_possible_boards(board : Board):
        nonlocal id
        possible_boards = set()
        for piece, x , y in board.pieces_positions:
            move_set = get_move_set(piece, x, y)

            for nx, ny in move_set:
                new_pieces_positions = list(board.pieces_positions)
                new_pieces_positions.remove((piece, x, y))
                new_pieces_positions.append((piece, nx, ny))
                possible_boards.add(Board(id, new_pieces_positions))
                id += 1
        
        return possible_boards
    
    id = 0
    initial_board = Board(id, pieces)
    id += 1
    visited_boards = set()
    visited_boards.add(initial_board)

    holes = set(holes)

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


    # for i, j in holes:
    #     pass

    DFS_boards(boards, True)
    return result

runtests(my_solve)
