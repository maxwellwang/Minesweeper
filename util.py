from random import randrange


def valid_coordinates(coordinates, d):
    """
    Checks if coordinates are in bounds.

    :param coordinates: tuple of i, j
    :param d: board dimension
    :return: if coordinates are in bounds
    """
    i, j = coordinates
    return 0 <= i < d and 0 <= j < d


def generate_board(d, n):
    """
    Generates a random d x d board containing n mines.

    :param d: dimension of board
    :param n: number of mines
    :return: completely covered d x d board, set of mine coordinates
    """
    if d <= 0:
        print(str(d) + ' is an invalid dimension')
        return
    if n < 0 or n >= d * d:
        print(str(n) + ' is an invalid number of mines')
        return

    board = []
    coordinates_list = []
    for i in range(d):
        board.append([])
        for j in range(d):
            board[i].append('?')
            coordinates_list.append((i, j))

    mines = set()
    for _ in range(n):
        i, j = coordinates_list.pop(randrange(0, len(coordinates_list)))
        mines.add((i, j))

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
    Checks if all cells are uncovered, marked as clear, or marked as mined.

    :param board: minesweeper board
    :return: if board has been completed
    """
    d = len(board)
    for row in board:
        for cell in row:
            if cell == '?':
                return False
    return True


def print_score(board, mines):
    """
    Calculates and prints score = # correctly flagged mines / # mines.

    :param board: minesweeper board
    :param mines: set of mine coordinates
    :return: nothing
    """
    num_correctly_flagged_mines = 0
    for i, j in mines:
        if board[i][j] == 'M':
            num_correctly_flagged_mines += 1
    score = round(num_correctly_flagged_mines / len(mines), 2)
    print('Score: ' + str(score))


def get_neighbor_coordinates(coordinates, d):
    """
    Get the coordinates of all neighbors.

    :param coordinates: i, j tuple
    :param d: board dimension
    :return: set of neighbor coordinates
    """
    neighbor_coordinates = set()
    i, j = coordinates
    for di in [-1, 0, 1]:
        for dj in [-1, 0, 1]:
            ni, nj = i + di, j + dj
            if (ni, nj) != (i, j) and valid_coordinates((ni, nj), d):
                neighbor_coordinates.add((ni, nj))
    return neighbor_coordinates


def get_clue(coordinates, mines, d):
    """
    Just queried safe cell, now get how many mines in neighbors.

    :param coordinates: i, j tuple
    :param mines: set of mines
    :return: number of mines around coordinates
    """
    clue = 0
    for neighbor_coordinates in get_neighbor_coordinates(coordinates, d):
        clue += 1 if neighbor_coordinates in mines else 0
    return clue


def query(coordinates, board, mines):
    """
    Uncovers cell on board. If mine, show the mine. If not, show clue.

    :param coordinates: cell coordinates to query
    :param board: minesweeper board
    :param mines: set of mines
    :return: new board
    """
    if not valid_coordinates(coordinates, len(board)):
        print(str(coordinates) + ' are invalid coordinates')
        return board
    i, j = coordinates
    if board[i][j] != '?':
        print(str(coordinates) + ' was already queried')
        return board

    if (i, j) in mines:
        board[i][j] = 'X'
    else:
        board[i][j] = str(get_clue((i, j), mines, len(board)))

    return board
