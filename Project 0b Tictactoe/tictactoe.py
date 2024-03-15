"""
Tic Tac Toe Player
"""

import math
import copy

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
    X_count = 0
    O_count = 0
    for row in board:
        for value in row:
            if value == X:
                X_count += 1
            elif value == O:
                O_count += 1

    turn = X_count - O_count
    if turn == 1:
        return O
    elif turn == 0:
        return X
    else:
        raise Exception('Board is not valid.')


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action[0], action[1]
    turn = player(board)

    if board[i][j] != EMPTY:
        raise Exception('Action is not valid.')
    elif i not in [0, 1, 2] or j not in [0, 1, 2]:
        raise Exception('Action is not valid.')
    
    resulted_board = copy.deepcopy(board)
    resulted_board[i][j] = turn

    return resulted_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for row in board:
      if row.count(X) == 3:
        return X
      if row.count(O) == 3:
        return O

    for j in range(3):
      column = ''
      for i in range(3):
        column += str(board[i][j])
      if column == 'XXX':
        return X
      if column == 'OOO':
        return O
    
    if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
        return board[1][1]
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    
    for row in board:
        for value in row:
            if value == EMPTY:
                return False
    
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    winner_player = winner(board)

    if not winner_player:
        return 0
    if winner_player == X:
        return 1
    if winner_player == O:
        return -1
    


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    if terminal(board):
        return None


    if player(board) == X:
        value, move = max_score(board)
        return move
    else:
        value, move = min_score(board)
        return move


def max_score(board):
    if terminal(board):
        return utility(board), None
    
    max_score = float('-inf')
    best_action = None

    for action in actions(board):
        score, opponent_action = min_score(result(board, action))
        if score > max_score:
            max_score = score
            best_action = action
    
    return max_score, best_action



def min_score(board):
    if terminal(board):
        return utility(board), None
    
    min_score = float('inf')
    best_action = None

    for action in actions(board):
        score, opponent_action = max_score(result(board, action))
        if score < min_score:
            min_score = score
            best_action = action
    
    return min_score, best_action




