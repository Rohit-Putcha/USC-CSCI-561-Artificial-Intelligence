from collections import defaultdict
from copy import deepcopy
import math
import random
import read
import write

class MyPlayer:
    def __init__(self):
        self.WHITE = 2
        self.BLACK = 1
        self.visited = defaultdict(list)
        self.pieces = defaultdict(list)
        self.group_liberties = defaultdict()

    # Count pieces of piece_type on board
    def count_pieces(self, board, piece_type):
        count = 0
        for i in range(5):
            for j in range(5):
                if board[i][j] == piece_type:
                    count += 1
                    coordinate = (i, j)
                    self.pieces[piece_type].append(coordinate)

        return count

    # Group liberty calculation of piece type on board
    def group_liberties_calculation(self, board, piece_type, black_pieces, white_pieces): 
        visited = {}
        keys = []
        pieces_list = black_pieces if piece_type == self.BLACK else white_pieces
        while pieces_list:
            coordinate_list = pieces_list[0]
            x = coordinate_list[0]
            y = coordinate_list[1]

            _, visited = self.count_liberties(
                board, x, y, piece_type, visited)

            newKeys = []
            for k, v in visited.items():
                if v == 0 and k not in keys:
                    keys.append(k)
                newKeys.append(k)

            pieces_list = list(set(pieces_list) - set(newKeys))

        return len(keys), keys

    # Manhattan distance of point i,j from all pieces of piece type
    def manhattan_distance(self, i, j, piece_type):
        return [[x,y] for x, y in self.pieces[piece_type] if abs(x-i) + abs(y-j) <= 2]

    '''def eval(self, i, j, board, piece_type, visited, pieces):
        self.pieces[3-piece_type] = None
        self.pieces[piece_type] = None

        minimizingPieceCount = self.count_pieces(
            board, 3 - piece_type, self.pieces[3 - piece_type])
        maximizingPieceCount = self.count_pieces(
            board, piece_type, self.pieces[piece_type])
        totalPieces = minimizingPieceCount + maximizingPieceCount

        boardScore = self.board_score(board, piece_type) + \
            minimizingPieceCount * self.count_liberties(board, i, j, 3 - piece_type, self.visited[3 - piece_type]) + \
            maximizingPieceCount * \
            self.count_liberties(board, i, j, piece_type,
                                self.visited[piece_type])'''

    # Minimax Alphabeta function
    def minimax_alphabeta(self, board, previous_board, cur_player, piece_type, alpha, beta, depth):
        put_down = False

        if (self.is_terminal(depth)):
            res = {}
            res[0] = None

            if cur_player == 0:
                if piece_type == self.BLACK:
                    res[1] = self.board_score(board, piece_type) - 2.5
                else:
                    res[1] = self.board_score(board, piece_type) + 2.5
            else:
                if piece_type == self.BLACK:
                    res[1] = self.board_score(board, 3-piece_type) + 2.5
                else:
                    res[1] = self.board_score(board, 3-piece_type) - 2.5

            return res
        
        expansion_order = self.setup_moves_order()
        MAX = -math.inf
        MIN = math.inf
        score_array = []
        calculated_score = ""
        calculated_move = ""

        for i in range(len(expansion_order)):
            intended_move = expansion_order[i]
            if board[intended_move[0]][intended_move[1]] != 0:
                continue

            new_board = self.clone_board(board)
            new_board[intended_move[0]][intended_move[1]] = piece_type

            liberty = self.count_liberties(
                new_board, intended_move[0], intended_move[1], piece_type, visited={})[0]

            num_of_pieces_eaten = 0
            if liberty == 0: # If liberty is 0, we can try to place piece and check if can capture opponent pieces
                pieces_eaten, new_board = self.remove_died_pieces(
                    new_board, 3-piece_type)

                num_of_pieces_eaten = len(pieces_eaten)

                if num_of_pieces_eaten > 0:
                    if not self.is_same_board(previous_board, new_board): # To check KO rule violation
                        put_down = True
                        opp_result = self.minimax_alphabeta(
                            new_board, board, 1-cur_player, 3-piece_type, alpha, beta, depth+1) # Check opponent move after my current move
                        current_move = {}
                        current_move[0] = '{},{}'.format(
                            intended_move[0], intended_move[1])
                        current_move[1] = opp_result[1]
                        score_array.append(current_move) #store current move and corresponding score in score array

                    else: # If KO rule is violated
                        continue

                else: # In case current move will lead to suicide
                    continue

            elif liberty > 0: # If piece has liberty
                put_down = True
                pieces_eaten, new_board = self.remove_died_pieces(
                    new_board, 3-piece_type) # if possible, we kill and update board

                opp_result = self.minimax_alphabeta(
                    new_board, board, 1-cur_player, 3-piece_type, alpha, beta, depth+1)
                current_move = {}
                current_move[0] = '{},{}'.format(intended_move[0], intended_move[1])
                current_move[1] = opp_result[1]
                score_array.append(current_move)

            cur_player_map, _ = self.num_of_endangered_places(new_board, piece_type)

            black_pieces, white_pieces = self.get_pieces_count(new_board)

            cur_player_group_liberties_count, cur_player_group_liberties = self.group_liberties_calculation(new_board, piece_type, black_pieces, white_pieces)
            opp_Player_group_liberties_count, opp_player_group_liberties = self.group_liberties_calculation(new_board, 3-piece_type, black_pieces, white_pieces)
                    
            endangered_score = (2 * len(cur_player_map.get(1))) if 1 in cur_player_map else 0

            cur_player_eye_count = self.num_of_eyes(new_board, piece_type, cur_player_group_liberties)
            opp_player_eye_count = self.num_of_eyes(new_board, 3 - piece_type, opp_player_group_liberties)
            
            if cur_player == 0: # Current player score
                for k in range(len(score_array)):
                    '''group_liberties_count = self.calGroupLiberties(cur_player, cur_playergroup_liberties_count, opPlayergroup_liberties_count)
                    eyesWeight = self.calGroupEyes(cur_player, cur_playerEyeMap, opPlayerEyeMap)'''
                    group_liberties_count = 0.25 * (cur_player_group_liberties_count - opp_Player_group_liberties_count)
                    eye_count = 0.25 * (cur_player_eye_count - opp_player_eye_count)

                    coordinate = str(score_array[k][0]).split(",")
                    x = int(coordinate[0])
                    y = int(coordinate[1])

                    current_score = float(score_array[k][1]) + 2 * num_of_pieces_eaten - endangered_score + \
                        self.board_score(new_board, piece_type) + group_liberties_count + eye_count

                    if MAX < current_score:
                        MAX = current_score
                        calculated_score = str(MAX)
                        calculated_move = score_array[k][0]
                        if beta <= MAX:
                            temp_result = {}
                            temp_result[0] = calculated_move
                            temp_result[1] = calculated_score
                            return temp_result

                        if alpha < MAX:
                            alpha = MAX

            elif cur_player == 1: # opponent score
                for k in range(len(score_array)):
                   
                    group_liberties_count = 0.25 * (cur_player_group_liberties_count - opp_Player_group_liberties_count)
                    eye_count = 0.25 * (opp_player_eye_count - opp_player_eye_count)

                    coordinate = str(score_array[k][0]).split(',')
                    x = int(coordinate[0])
                    y = int(coordinate[1])

                    current_score = float(score_array[k][1]) - 2 * num_of_pieces_eaten + endangered_score + \
                        self.board_score(new_board, 3-piece_type) - group_liberties_count - eye_count

                    if MIN > current_score:
                        MIN = current_score
                        calculated_score = str(MIN)
                        calculated_move = score_array[k][0]

                        if alpha >= MIN:
                            temp_result = {}
                            temp_result[0] = calculated_move
                            temp_result[1] = calculated_score
                            return temp_result

                        if beta > MIN:
                            beta = MIN

        res = {}
        if not put_down: # If no valid move available, we pass the move
            res[0] = "PASS"
            if cur_player == 0:
                if piece_type == self.BLACK:
                    res[1] = self.board_score(board, piece_type) - 2.5
                else:
                    res[1] = self.board_score(board, piece_type) + 2.5
            else:
                if piece_type == self.BLACK:
                    res[1] = self.board_score(board, 3-piece_type) + 2.5
                else:
                    res[1] = self.board_score(board, 3-piece_type) - 2.5

        else:
            res[0] = calculated_move
            res[1] = calculated_score

        return res

    '''def remove_dead_pieces(self, new_board, intended_move, piece_type):
        canCaptureTop, canCaptureBottom, canCaptureRight, canCaptureLeft = False, False, False, False
        visitedTop = {}
        if self.count_liberties(new_board, intended_move[0]-1, intended_move[1], 3-piece_type, visitedTop) == 0:
            canCaptureTop = True

        visitedBottom = {}
        if self.count_liberties(new_board, intended_move[0]+1, intended_move[1], 3-piece_type, visitedBottom) == 0:
            canCaptureBottom = True

        visitedRight = {}
        if self.count_liberties(new_board, intended_move[0], intended_move[1] + 1, 3-piece_type, visitedRight) == 0:
            canCaptureRight = True

        visitedLeft = {}
        if self.count_liberties(new_board, intended_move[0], intended_move[1] - 1, 3-piece_type, visitedLeft) == 0:
            canCaptureLeft = True

        eatenStones = []
        if canCaptureTop:
            for pos in visitedTop:
                if pos not in eatenStones:
                    eatenStones.append(pos)

        if canCaptureBottom:
            for pos in visitedBottom:
                if pos not in eatenStones:
                    eatenStones.append(pos)

        if canCaptureLeft:
            for pos in visitedLeft:
                if pos not in eatenStones:
                    eatenStones.append(pos)

        if canCaptureRight:
            for pos in visitedRight:
                if pos not in eatenStones:
                    eatenStones.append(pos)

        self.capture(new_board, eatenStones)
        return len(eatenStones)'''

    # Num of endangered places for piece type on board
    def num_of_endangered_places(self, board, piece_type):
        map = defaultdict(list)
        liberty_map = defaultdict(list)
        visited = []
        for i in range(5):
            for j in range(5):
                coordinate = (i, j)
                if board[i][j] == piece_type and coordinate not in visited:
                    tmp = {}
                    liberty, tmp = self.count_liberties(
                        board, i, j, piece_type, tmp)
                    for pos, value in tmp.items():
                        if pos not in visited and value == 1:
                            visited.append(pos)
                            map[liberty].append(pos)

                        if value == 0:
                            liberty_map[liberty].append(pos)
                        
        return map, liberty_map

    # Count single or group liberties of point i, j of piece type 
    def count_liberties(self, board, i, j, piece_type, visited = {}):
        count = 0
        coordinate = (i, j)
        if i < 0 or i > 4 or j < 0 or j > 4 or board[i][j] == 3 - piece_type or coordinate in visited:
            return 0, visited

        if board[i][j] == 0:
            visited[coordinate] = 0
            return 1, visited

        visited[coordinate] = 1

        count += self.count_liberties(board, i+1, j, piece_type, visited)[0] + \
            self.count_liberties(board, i-1, j, piece_type, visited)[0] + \
            self.count_liberties(board, i, j+1, piece_type, visited)[0] + \
            self.count_liberties(board, i, j-1, piece_type, visited)[0]

        return count, visited

    # Clone board utilised from host
    def clone_board(self, board):
        return deepcopy(board)

    # Check if previous board and present board are same
    def is_same_board(self, board, previous_board):
        for i in range(5):
            for j in range(5):
                if board[i][j] != previous_board[i][j]:
                    return False
        
        return True
    
    # Capture set of pieces from board
    def capture(self, board, set: list):
        if len(set) == 0:
            return
        
        for s in set:
            i = int(s[0])
            j = int(s[1])
            board[i][j] = 0

    # Calculate board score for piece type
    def board_score(self, board, piece_type):
        white_count, black_count = 0, 0
        for i in range(5):
            for j in range(5):
                if board[i][j] == self.BLACK:
                    black_count += 1
                if board[i][j] == self.WHITE:
                    white_count += 1

        if piece_type == self.WHITE:
            return white_count - black_count
        else:
            return black_count - white_count
        
    # Initial moves order
    def setup_moves_order(self):
        expansion_order = [(2,2), (1,1), (1,3), (3,1), (3,3), \
                            (2,0), (2,4), (0,4), (4,2), (0,1), \
                            (0,3), (1,4), (3,4), (4,3), (4,1), \
                            (3,0), (1,0) , (1,2), (3,2), (2,1), \
                            (2,3), (0,0), (4,4), (0,4), (4,0) ]
        
        return expansion_order

    # Check if terminal depth
    def is_terminal(self, depth):
        return depth >= 4

    # Count the number of eyes of piece type in board
    def num_of_eyes(self, board, piece_type, pieces: defaultdict(list)):
        eye_count = 0
        for node in pieces:
            top_line, bottom_line, right_line, left_line = False, False, False, False
            x = node[0]
            y = node[1]

            if x == 0:
                top_line = True
            
            if x == 4:
                bottom_line = True
            
            if y == 0:
                left_line = True
            
            if y == 4:
                right_line = True

            if not top_line and not bottom_line and not right_line and not left_line:
                if board[x-1][y] == piece_type and board[x+1][y] == piece_type and \
                    board[x][y+1] == piece_type and board[x][y-1] == piece_type:
                    eye_count += 1
                
            if top_line:
                if right_line:
                    if board[x+1][y] == piece_type and board[x][y-1] == piece_type:
                        eye_count += 1
                elif left_line:
                    if board[x+1][y] == piece_type and board[x][y+1] == piece_type:
                        eye_count += 1
                else:
                    if board[x+1][y] == piece_type and board[x][y+1] == piece_type and board[x][y-1] == piece_type:
                        eye_count += 1
            
            elif bottom_line:
                if right_line:
                    if board[x-1][y] == piece_type and board[x][y-1] == piece_type:
                        eye_count += 1
                elif left_line:
                    if board[x-1][y] == piece_type and board[x][y+1] == piece_type:
                        eye_count += 1
                else:
                    if board[x-1][y] == piece_type and board[x][y+1] == piece_type and board[x][y-1] == piece_type:
                        eye_count += 1

            elif left_line:
                if board[x-1][y] == piece_type and board[x][y+1] == piece_type and board[x+1][y] == piece_type:
                    eye_count += 1

            elif right_line:
                if board[x-1][y] == piece_type and board[x+1][y] == piece_type and board[x][y-1] == piece_type:
                    eye_count += 1

        return eye_count

    # Get pieces count on board of black and white pieces
    def get_pieces_count(self, board):
        black_pieces, white_pieces = [], []

        for i in range(5):
            for j in range(5):
                if board[i][j] == self.BLACK:
                    black_pieces.append((i, j))

                elif board[i][j] == self.WHITE:
                    white_pieces.append((i, j))

        return black_pieces, white_pieces

    # Valid Place Check method utilised from host
    def valid_place_check(self, board, i, j, piece_type):
        '''
        Check whether a placement is valid.

        :param i: row number of the board.
        :param j: column number of the board.
        :param piece_type: 1(white piece) or 2(black piece).
        :param test_check: boolean if it's a test check.
        :return: boolean indicating whether the placement is valid.
        '''

        # Check if the place is in the board range and the place is already filled with any piece
        if not (i >= 0 and i < len(board)) or not (j >= 0 and j < len(board)) or board[i][j] != 0:
            return False
        
        test_board = self.clone_board(board)

        # Check if the place has liberty
        test_board[i][j] = piece_type
        if self.find_liberty(test_board, i, j):
            return True

        # If not, remove the died pieces of opponent and check again
        died_pieces = self.remove_died_pieces(test_board, 3 - piece_type)
        if not self.find_liberty(test_board, i, j):
            return False

        # Check special case: repeat placement causing the repeat board state (KO rule)
        else:
            if died_pieces and self.is_same_board(self.previous_board, test_board):
                return False
        return True

    # Find Liberty for point i,j method utilised from host
    def find_liberty(self, board, i, j):
        '''
        Find liberty of a given stone. If a group of allied pieces has no liberty, they all die.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: boolean indicating whether the given stone still has liberty.
        '''

        ally_members = self.ally_dfs(board, i, j)
        for member in ally_members:
            neighbors = self.detect_neighbor(board, member[0], member[1])
            for piece in neighbors:
                # If there is empty space around a piece, it has liberty
                if board[piece[0]][piece[1]] == 0:
                    return True
        # If none of the pieces in a allied group has an empty space, it has no liberty
        return False

    # Find died pieces of piece_type on board method utilised from host
    def find_died_pieces(self, board, piece_type):
        '''
        Find the died pieces that has no liberty in the board for a given piece type.

        :param piece_type: 1('X') or 2('O').
        :return: a list containing the dead pieces row and column(row, column).
        '''

        died_pieces = []

        for i in range(len(board)):
            for j in range(len(board)):
                # Check if there is a piece at this position:
                if board[i][j] == piece_type:
                    # The piece die if it has no liberty
                    if not self.find_liberty(board, i, j):
                        died_pieces.append((i,j))
        return died_pieces

    # Remove died pieces of piece_type on board method utilised from host
    def remove_died_pieces(self, board, piece_type):
        '''
        Remove the dead pieces in the board.

        :param piece_type: 1('X') or 2('O').
        :return: locations of dead pieces.
        '''

        died_pieces = self.find_died_pieces(board, piece_type)
        if not died_pieces: return [], board
        test_board = self.remove_certain_pieces(board, died_pieces)
        return died_pieces, test_board

    # Remove given positions from board method utilised from host
    def remove_certain_pieces(self, board, positions):
        '''
        Remove the stones of certain locations.

        :param positions: a list containing the pieces to be removed row and column(row, column)
        :return: None.
        '''
        for piece in positions:
            board[piece[0]][piece[1]] = 0

        return board

    # Detect neighbor method utilised from host
    def detect_neighbor(self, board, i, j):
        '''
        Detect all the neighbors of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the neighbors row and column (row, column) of position (i, j).
        '''

        neighbors = []
        # Detect borders and add neighbor coordinates
        if i > 0: neighbors.append((i-1, j))
        if i < len(board) - 1: neighbors.append((i+1, j))
        if j > 0: neighbors.append((i, j-1))
        if j < len(board) - 1: neighbors.append((i, j+1))
        return neighbors

    # Detect neighbor ally method utilised from host
    def detect_neighbor_ally(self, board, i, j):
        '''
        Detect the neighbor allies of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the neighbored allies row and column (row, column) of position (i, j).
        '''

        neighbors = self.detect_neighbor(board, i, j)  # Detect neighbors
        group_allies = []
        # Iterate through neighbors
        for piece in neighbors:
            # Add to allies list if having the same color
            if board[piece[0]][piece[1]] == board[i][j]:
                group_allies.append(piece)
        return group_allies

    # Perform ally dfs method utilised from host
    def ally_dfs(self, board, i, j):
        '''
        Using DFS to search for all allies of a given stone.

        :param i: row number of the board.
        :param j: column number of the board.
        :return: a list containing the all allies row and column (row, column) of position (i, j).
        '''
        stack = [(i, j)]  # stack for DFS serach
        ally_members = []  # record allies positions during the search
        while stack:
            piece = stack.pop()
            ally_members.append(piece)
            neighbor_allies = self.detect_neighbor_ally(board, piece[0], piece[1])
            for ally in neighbor_allies:
                if ally not in stack and ally not in ally_members:
                    stack.append(ally)
        return ally_members

    '''def find_all_neighbors(self, curr_move):
        temp = []
        for change in [(1,0), (-1,0), (0,1), (0,-1)]:
            if (0 <= curr_move[0]+change[0] < 5) and (0 <= curr_move[1]+change[1] < 5):
                temp.append((curr_move[0]+change[0], curr_move[1]+change[1]))
        return temp'''

    '''def find_empty_neighbor(self, board, neighbours):
        empty_x = []
        for neighbor in neighbours:
            if board[neighbor[0]][neighbor[1]]==0:
                empty_x.append(neighbor)
        return empty_x'''

    # Find available spaces on board
    def find_avail_spaces(self, board):
        temp = list()
        for i in range(5):
            for j in range(5):
                if board[i][j] == 0:
                    temp.append((i, j))

        return temp

    # Find killer moves on board
    def find_killer_moves_count(self, board, avail_spaces, piece_type):
        kill_move_count = dict()
        for space in avail_spaces:
            board[space[0]][space[1]] = piece_type
            died_pieces = self.find_died_pieces(board, 3-piece_type)
            board[space[0]][space[1]] = 0
            if len(died_pieces) >= 1:
                kill_move_count[space] = len(died_pieces)

        sorted_kill_move_count = sorted(
            kill_move_count, key=kill_move_count.get, reverse=True)

        return sorted_kill_move_count

    # Find moves to be removed from board
    def find_moves_to_be_removed(self, board, avail_moves, piece_type):
        moves_to_be_removed = list()
        for i in avail_moves:
            board[i[0]][i[1]] = piece_type
            opp_move = self.unoccupied_position(board, 3-piece_type)
            for j in opp_move:
                board[j[0]][j[1]] = 3 - piece_type
                died_pieces = self.find_died_pieces([], piece_type)
                board[j[0]][j[1]] = 0
                if i in died_pieces:
                    moves_to_be_removed.append(i)
            board[i[0]][i[1]] = 0

        return moves_to_be_removed

    # Find Safe moves on board
    def find_safe_moves(self, board, piece_type):
        safe_moves = dict()
        opp_moves = list()
        for i in range(5):
            for j in range(5):
                if board[i][j] == 0:
                    opp_moves.append((i, j))

        for i in opp_moves:
            board[i[0]][i[1]] = 3-piece_type
            current_died_pieces = self.find_died_pieces(board, piece_type)
            board[i[0]][i[1]] = 0
            if len(current_died_pieces) >= 1:
                safe_moves[i] = len(current_died_pieces)

        sorted_safe_moves = sorted(safe_moves, key=safe_moves.get, reverse=True)
        return sorted_safe_moves

    # Find unoccupied positions on board
    def unoccupied_position(self, new_go_board, piece_type):
        # Check valid moves for the current player (board)
            valid_move = []
            for i in range(5):
                for j in range(5):
                    if self.valid_place_check(new_go_board, i, j, piece_type):
                        valid_move.append((i, j))
            return random.sample(valid_move, len(valid_move))

    # Set move on board of piece type
    def set_move(self, board, previous_board, piece_type):

        # Find Killer Moves
        avail_spaces = self.find_avail_spaces(board)

        sorted_kill_move_count = self.find_killer_moves_count(board, avail_spaces, piece_type)

        for i in sorted_kill_move_count:
            # lets start here
            test_go_game_board = deepcopy(board)
            test_go_game_board[i[0]][i[1]] = piece_type
            died_piece = self.find_died_pieces(test_go_game_board, 3 - piece_type)
            for x in died_piece:
                test_go_game_board[x[0]][x[1]] = 0

            if i != None and self.previous_board != test_go_game_board:
                return i

        avail_moves = self.unoccupied_position(board, piece_type)

        moves_to_be_removed = self.find_moves_to_be_removed(board, avail_moves, piece_type)

        for x in moves_to_be_removed:
            if x in avail_moves:
                avail_moves.remove(x)

        if len(avail_moves) == 0:
            return "PASS"

        sorted_safe_moves = self.find_safe_moves(board, piece_type)

        for i in sorted_safe_moves:
            if i != None and i in avail_moves:
                return i

        moves_order = self.setup_moves_order()
        if len(avail_moves) >= 15:
            for itx, value in enumerate(moves_order):
                if value in avail_moves and itx < 9:
                    return value

        # Call Minimax alphabeta
        result = self.minimax_alphabeta(board, previous_board, 0, piece_type, -math.inf, math.inf, 0)
        x, y = result[0].split(",")
        return(x, y)

if __name__ == "__main__":
    player = MyPlayer()
    player.piece_type, player.previous_board, player.board = read.readInput()
    result = player.set_move(player.board, player.previous_board, player.piece_type)
    write.writeOutput('{},{}'.format(result[0], result[1]))