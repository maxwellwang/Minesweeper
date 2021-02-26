from random import randint


class Cell:
    mine = False
    covered = True
    clue = 0
    num_safe = 0
    num_mines = 0
    num_hidden = 0

    def __init__(self, num_hidden):
        self.num_hidden = num_hidden

    def __str__(self):
        if self.covered:
            return "."
        if self.mine:
            return "M"
        return str(self.clue)


def num_neighbors(cell, d):
    """
    Calculates number of neighbors around cell

    :param cell: coordinates of cell
    :param d: dimension of board
    :return: number of neighbors around cell
    """
    x, y = cell
    num = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx != 0 or dy != 0) and 0 <= x + dx < d and 0 <= y + dy < d:
                num += 1
    return num


def get_neighbors(cell, d):
    """
    Gets coordinates of neighbors around cell

    :param cell: coordinates of cell
    :param d: dimension of board
    :return: coordinates of neighbors around cell
    """
    x, y = cell
    neighbors = set()
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx != 0 or dy != 0) and 0 <= x + dx < d and 0 <= y + dy < d:
                neighbors.add((x + dx, y + dy))
    return neighbors


def generate_board(d, n):
    """
    Generates a random d x d board containing n mines. Each cell will keep track of:
    1. whether or not it is a mine or safe
    2. whether or not it is currently covered
    3. if safe, the number of mines surrounding it indicated by the clue
    4. the number of safe squares identified around it
    5. the number of mines identified around it
    6. the number of hidden squares around it

    :param d: dimension of board
    :param n: number of mines
    :return: d x d board containing n mines
    """
    if d <= 0:
        print('Invalid dimension')
        return None
    if n < 0 or n >= d * d:
        print('Invalid number of mines')
        return None

    board = [[Cell(num_neighbors((x, y), d)) for y in range(d)] for x in range(d)]

    mines = set()
    for _ in range(n):
        x, y = randint(0, d - 1), randint(0, d - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            board[x][y].mine = True
            for neighbor in get_neighbors((x, y), d):
                nx, ny = neighbor
                board[nx][ny].clue += 1

    return board


def print_board(board):
    for row in board:
        print(' '.join(str(cell) for cell in row))
