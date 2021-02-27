from util import *

d = 3
n = 3
board, mines = generate_board(d, n)
print_board(board)
print(mines)
while True:
    print_board(board)
    coordinates = input('enter coordinates as x,y: ')
    x, y = coordinates.split(',')
    x, y = int(x), int(y)
    board = query((x, y), board, mines)
