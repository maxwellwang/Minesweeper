from util import *

d = 3
n = 3
board, mines = generate_board(d, n)
print(mines)
while not completed(board):
    print_board(board)
    coordinates = input('enter coordinates as x,y: ')
    i, j = coordinates.split(',')
    i, j = int(i), int(j)
    board = query((i, j), board, mines)
