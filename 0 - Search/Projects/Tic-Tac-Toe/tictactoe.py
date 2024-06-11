"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    flat_board = [cell for row in board for cell in row] 
    x_count = flat_board.count(X)
    o_count = flat_board.count(O)
    return X if x_count == o_count else O
        

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for row in range(len(board)): 
        for col in range(len(board[row])): 
            if board[row][col] == EMPTY: 
                possible_actions.add((row, col))
    return possible_actions


class NotAValidAction(Exception):
    def __init__(self, message):
        super().__init__(message)


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action 
    if i > 2 or i < 0 or j > 2 or j < 0: 
        raise NotAValidAction("not a valid action.")
    else: 
        new_board = [row[:] for row in board]
        new_board[i][j] = player(new_board)
        return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check rows 
    for row in board: 
        if len(set(row)) == 1 and row[0] != EMPTY: 
            return row[0]
    
    # check columns 
    for col in range(3): 
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != EMPTY: 
            return board[0][col]
        
    # check diagonals 
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != EMPTY: 
        return board[0][0]
    if board [0][2] == board[1][1] == board[2][0] and board[0][2] != EMPTY: 
        return board[0][2]
    
    else: 
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # check if winner exists 
    if winner(board): 
        return True
    # check draw 
    if all(cell != EMPTY for row in board for cell in row): 
        return True 
    # otherwise game not over 
    return False 


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X: 
        return 1 
    elif winner(board) == O: 
        return -1 
    else: 
        return 0 


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board): 
        return None 
    else: 
        # check whose turn it is 
        current_player = player(board) 
        is_maximizing = current_player == X 

        best_move = None 

        if is_maximizing: 
            best_score = float('-inf')
            possible_actions = actions(board)
            for action in actions(board): 
                temp_board = result(board, action) 
                score = minimax_score(temp_board, False)
                if score > best_score: 
                    best_score = score 
                    best_move = action 
        else: 
            best_score = float('inf')
            possible_actions = actions(board)
            for action in actions(board): 
                temp_board = result(board, action) 
                score = minimax_score(temp_board, True)
                if score < best_score: 
                    best_score = score 
                    best_move = action 
        return best_move
    
def minimax_score(board, is_maximizing):
    if terminal(board):
        return terminal(board)

    if is_maximizing:
        best_score = float('-inf')
        possible_actions = actions(board)
        for action in possible_actions:
            new_board = result(board, action)
            score = minimax_score(new_board, False)
            best_score = max(best_score, score)
    else:
        best_score = float('inf')
        possible_actions = actions(board)
        for action in possible_actions:
            new_board = result(board, action)
            score = minimax_score(new_board, True)
            best_score = min(best_score, score)
    
    return best_score