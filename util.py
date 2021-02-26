from random import randint


class Cell:
    mine = False
    covered = True
    clue = 0
    num_safe = 0
    num_mines = 0
    num_hidden = 0
    safe_flag = False
    mine_flag = False

    def __init__(self, num_hidden):
        self.num_hidden = num_hidden

    def __str__(self):
        if self.covered:
            if self.safe_flag:
                return 'S'
            elif self.mine_flag:
                return 'F'
            else:
                return '.'
        elif self.mine:
            return 'M'
        else:
            return str(self.clue)


def valid_coordinates(coordinates, d):
    """
    Checks if coordinates are in bounds.

    :param coordinates: tuple of x, y
    :param d: board dimension
    :return: if coordinates are in bounds
    """
    x, y = coordinates
    return 0 <= x < d and 0 <= y < d


def num_neighbors(coordinates, d):
    """
    Calculates number of neighbors around cell.

    :param coordinates: coordinates of cell
    :param d: dimension of board
    :return: number of neighbors around cell
    """
    x, y = coordinates
    num = 0
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx != 0 or dy != 0) and 0 <= x + dx < d and 0 <= y + dy < d:
                num += 1
    return num


def get_neighbors(coordinates, d):
    """
    Gets coordinates of neighbors around cell.

    :param coordinates: coordinates of cell
    :param d: dimension of board
    :return: coordinates of neighbors around cell
    """
    x, y = coordinates
    neighbors = set()
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if (dx != 0 or dy != 0) and 0 <= x + dx < d and 0 <= y + dy < d:
                neighbors.add((x + dx, y + dy))
    return neighbors


def generate_board(d, n):
    """
    Generates a random d x d board containing n mines. Each cell will keep track of:
    1. whether or not it is a mine or safe.
    2. whether or not it is currently covered.
    3. if safe, the number of mines surrounding it indicated by the clue.
    4. the number of safe squares identified around it.
    5. the number of mines identified around it.
    6. the number of hidden squares around it.
    7. if it is flagged as safe.
    8. if it is flagged as a mine.

    :param d: dimension of board
    :param n: number of mines
    :return: d x d board containing n mines, set of mine coordinates
    """
    if d <= 0:
        print('Invalid dimension')
        return None
    if n < 0 or n >= d * d:
        print('Invalid number of mines')
        return None

    board = [[Cell(num_neighbors((x, y), d)) for y in range(d)] for x in range(d)]

    mines = set()
    while len(mines) < n:
        x, y = randint(0, d - 1), randint(0, d - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            board[x][y].mine = True
            for neighbor in get_neighbors((x, y), d):
                nx, ny = neighbor
                board[nx][ny].clue += 1

    return board, mines


def print_board(board):
    """
    Prints out board.

    :param board: minesweeper board to print out
    :return: nothing
    """
    for row in board:
        print(' '.join(str(cell) for cell in row))


def completed(board):
    """
    Checks if all safe cells have been queried.

    :param board: minesweeper board
    :return: if board has been completed
    """
    d = len(board)
    for x in range(d):
        for y in range(d):
            cell = board[x][y]
            if cell.covered and not cell.safe_flag and not cell.mine_flag:
                return False
    return True


def score(board, mines):
    """
    Calculates score = # correctly flagged mines / # mines.
    :param board: minesweeper board
    :param mines: set of mine coordinates
    :return: # correctly flagged mines / # mines
    """
    num_correctly_flagged_mines = 0
    for coordinates in mines:
        x, y = coordinates
        cell = board[x][y]
        if cell.mine_flag:
            num_correctly_flagged_mines += 1
    return num_correctly_flagged_mines / len(mines)


def query(coordinates, board, mines):
    """
    Uncovers cell on board. If mine, show the mine. If not, show clue.

    :param coordinates: cell coordinates to query
    :param board: minesweeper board
    :return: new board
    """
    if not valid_coordinates(coordinates, len(board)):
        print('Invalid coordinates')
        return board
    x, y = coordinates
    cell = board[x][y]
    if not cell.covered:
        print('Cell was already queried')
        return board
    cell.covered = False
    if completed(board):
        print(score(board, mines))
    return board
