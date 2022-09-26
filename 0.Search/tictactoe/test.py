from multiprocessing import Barrier
from tkinter import E
from tictactoe import *

X = "X"
O = "O"
EMPTY = None


board = [[X, X, O],
            [O, EMPTY, O],
            [EMPTY, EMPTY, EMPTY]]

print(minimizingPlayer(board, float('-inf'), float('inf')))
print(player(board))
#print(maximizingPlayer(board, float('-inf'), float('inf')))
