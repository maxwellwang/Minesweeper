from util import *

d = 3
n = 3
board, mines = generate_board(d, n)
print_board(board)
print(mines)
while True:
    coordinates = input('coordinates: ')
    x, y = coordinates.split(',')
    x, y = int(x), int(y)
    board = query((x, y), board, mines)
    print_board(board)
