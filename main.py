from util import *

d = 3
n = 3
board = generate_board(d, n)
# uncover whole board so we can see mines and clues
for x in range(d):
    for y in range(d):
        board[x][y].covered = False
print_board(board)
