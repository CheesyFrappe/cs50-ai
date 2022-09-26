"""
Tic Tac Toe Player
"""

from math import inf
from decimal import InvalidOperation
from hashlib import new
import math, copy
import re

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
    total = 0
    
    for i in range(3):
        for j in range(3):
            if board[i][j] != EMPTY:
                total += 1

    # X player begins (first)
    if board == initial_state():
        return X

    if total % 2 == 1:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action = set()
    # i stands for row
    for i in range(3):
        # j stands for column
        for j in range(3):  
            if board[i][j] == EMPTY:
                action.add((i, j))

    return action


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """

    # assume that minimax returns coordinates as a tuple (list maybe, i dunno) :)
    i = action[0]
    j = action[1]

    if board[i][j] is not EMPTY:
        raise "InvalidAction"
    
    # save the original board
    new_board = copy.deepcopy(board)

    if player(board) == X:
        new_board[i][j] = X
    else:
        new_board[i][j] = O
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # getting same vertical values in same lists
    transpose_board = list(map(list, zip(*board)))

    # getting same diagonal values in same lists
    left_diagonal = [board[0][0], board[1][1], board[2][2]]
    right_diagonal = [board[0][2], board[1][1], board[2][0]]
    
    result_left_diagonal = left_diagonal.count(left_diagonal[0]) == 3
    result_right_diagonal = right_diagonal.count(right_diagonal[0]) == 3
        
    if result_right_diagonal: return right_diagonal[0]
    if result_left_diagonal: return left_diagonal[0]

    # checking horizontally
    for i in range(3):

        # checks whether there are empty rows or columns
        if EMPTY in board[i]:
            continue
        result_horizontally = board[i].count(board[i][0]) == 3
        if result_horizontally: return board[i][0]
    
    # checking vertically
    for i in range(3):
        if EMPTY in transpose_board[i]:
            continue
        result_vertically = transpose_board[i].count(transpose_board[i][0]) == 3
        if result_vertically: return transpose_board[i][0]
    
    return None
    

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    total = 0
    for i in range(3):
        if not EMPTY in board[i]:
            continue
        total += board[i].count(EMPTY)

    if winner(board) == X or winner(board) == O or total == 0:
        return True
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


# X => Max 
# O => Min
def minimax(board):
    if terminal(board):
        return None
    
    if player(board) == X:
        return maximizingPlayer(board, float(-inf), float(inf))[1]
    else:
        return minimizingPlayer(board, float(-inf), float(inf))[1]


def maximizingPlayer(board, alpha, beta):
    if terminal(board):
        return [utility(board), None]

    move = None
    max_eval = float('-inf')

    for action in actions(board):
        eval = minimizingPlayer(result(board, action), alpha, beta)[0]
        alpha = max(alpha, eval)
        if eval > max_eval:
            max_eval = eval
            move = action
        if beta <= alpha:
            break
    
    return [max_eval, move];


def minimizingPlayer(board, alpha, beta):
    if terminal(board):
        return [utility(board), None]
    
    move = None
    min_eval = float('inf')
    
    for action in actions(board):
        eval = maximizingPlayer(result(board, action), alpha, beta)[0]
        beta = min(beta, eval)
        if eval < min_eval:
            min_eval = eval
            move = action
        if beta <= alpha:
            break
    
    return [min_eval, move];
