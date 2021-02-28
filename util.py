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
    if board[i][j].isdigit() or board[i][j] == 'X':
        print(str(coordinates) + ' was already queried')
        return board
    if board[i][j] == 'M':
        print(str(coordinates) + ' was flagged as mined, we shouldn\'t search it')
        return board

    board[i][j] = 'X' if (i, j) in mines else str(get_clue((i, j), mines, len(board)))

    return board


def random_query(board, mines):
    """
    Randomly queries hidden cell on board.

    :param board: minesweeper board
    :param mines: set of mine coordinates
    :return: new board, random coordinates queried
    """
    d = len(board)
    hidden_coordinates_list = []
    for i in range(d):
        for j in range(d):
            if board[i][j] == '?':
                hidden_coordinates_list.append((i, j))
    i, j = hidden_coordinates_list[randrange(0, len(hidden_coordinates_list))]
    return query((i, j), board, mines), (i, j)


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


def get_score(board, mines):
    """
    Calculates and prints score = # correctly flagged mines / # mines.

    :param board: minesweeper board
    :param mines: set of mine coordinates
    :return: # correctly flagged mines / # mines
    """
    num_correctly_flagged_mines = 0
    for i, j in mines:
        if board[i][j] == 'M':
            num_correctly_flagged_mines += 1
    return round(num_correctly_flagged_mines / len(mines), 2)


class BasicAgent:
    def __init__(self, arg1, arg2):
        """
        Prepare the info that basic agent needs to make inferences. This can be initialized using d, n or board, mines.

        :param arg1: either d: board dimension, or board: minesweeper board
        :param arg2: either n: number of mines, or mines: set of mines
        """
        if isinstance(arg1, int) and isinstance(arg2, int):
            d, n = arg1, arg2
            board, mines = generate_board(d, n)
        else:
            board, mines = arg1, arg2
        self.board = board
        self.mines = mines
        d = len(board)
        self.num_safe_board = [[0 for _ in range(d)] for _ in range(d)]
        self.num_mines_board = [[0 for _ in range(d)] for _ in range(d)]
        self.num_hidden_board = [[len(get_neighbor_coordinates((i, j), d)) for j in range(d)] for i in range(d)]
        self.score = 0

    def infer(self):
        """
        Use individual cell inference to mark hidden cells as safe or mined. If we can mark any safe cells and the board
        hasn't been completed yet, repeat inference.

        :return: nothing
        """
        d = len(self.board)
        new_clues = False  # new clue(s) revealed: if board isn't completed then we should infer again
        for i in range(d):
            for j in range(d):
                if self.board[i][j].isdigit():
                    if int(self.board[i][j]) - self.num_mines_board[i][j] == self.num_hidden_board[i][j]:
                        # every hidden neighbor is a mine
                        for ni, nj in get_neighbor_coordinates((i, j), d):
                            if self.board[ni][nj] == '?':
                                self.board[ni][nj] = 'M'
                                for ni2, nj2 in get_neighbor_coordinates((ni, nj), d):
                                    self.num_mines_board[ni2][nj2] += 1
                    elif len(get_neighbor_coordinates((i, j), d)) - int(self.board[i][j]) - self.num_safe_board[i][j] == \
                            self.num_hidden_board[i][j]:
                        # every hidden neighbor is safe
                        for ni, nj in get_neighbor_coordinates((i, j), d):
                            if self.board[ni][nj] == '?':
                                self.board[ni][nj] = 'C'
                                self.board = query((ni, nj), self.board, self.mines)
                                new_clues = True
                                for ni2, nj2 in get_neighbor_coordinates((ni, nj), d):
                                    self.num_safe_board[ni2][nj2] += 1
                                    self.num_hidden_board[ni2][nj2] -= 1
        if new_clues and not completed(self.board):
            self.infer()

    def run(self):
        """
        Runs basic agent on the minesweeper board, and prints final score.

        :return: nothing
        """
        d = len(self.board)
        while not completed(self.board):
            self.infer()
            if not completed(self.board):
                # reveal random cell and update info
                self.board, (i, j) = random_query(self.board, self.mines)
                for ni, nj in get_neighbor_coordinates((i, j), d):
                    if self.board[i][j] == 'X':
                        # blew up mine, update neighbor's info appropriately
                        self.num_mines_board[ni][nj] += 1
                    else:
                        # found safe cell, update neighbor's info appropriately
                        self.num_safe_board[ni][nj] += 1
                    self.num_hidden_board[ni][nj] -= 1
        self.score = get_score(self.board, self.mines)
        print('Score: ' + str(self.score))


class ImprovedAgent:
    def __init__(self, arg1, arg2):
        """
        Prepare the info that improved agent needs to make inferences. This can be initialized using d, n or board,
        mines.

        :param arg1: either d: board dimension, or board: minesweeper board
        :param arg2: either n: number of mines, or mines: set of mines
        """
        if isinstance(arg1, int) and isinstance(arg2, int):
            d, n = arg1, arg2
            board, mines = generate_board(d, n)
        else:
            board, mines = arg1, arg2
        self.board = board
        self.mines = mines
        d = len(board)
        self.num_safe_board = [[0 for _ in range(d)] for _ in range(d)]
        self.num_mines_board = [[0 for _ in range(d)] for _ in range(d)]
        self.num_hidden_board = [[len(get_neighbor_coordinates((i, j), d)) for j in range(d)] for i in range(d)]
        # TODO: define some kind of dictionary to hold equations that we can manipulate to infer more than basic agent
        self.score = 0

    def infer(self):
        """
        TODO: use combo of individual cell inference and equations to infer safe and mined cells

        :return: nothing
        """

    def run(self):
        """
        Runs improved agent on the minesweeper board, and prints final score.

        :return: nothing
        """
        d = len(self.board)
        while not completed(self.board):
            self.infer()
            if not completed(self.board):
                # reveal random cell and update info
                self.board, (i, j) = random_query(self.board, self.mines)
                for ni, nj in get_neighbor_coordinates((i, j), d):
                    if self.board[i][j] == 'X':
                        # blew up mine, update neighbor's info appropriately
                        self.num_mines_board[ni][nj] += 1
                    else:
                        # found safe cell, update neighbor's info appropriately
                        self.num_safe_board[ni][nj] += 1
                    self.num_hidden_board[ni][nj] -= 1
        self.score = get_score(self.board, self.mines)
        print('Score: ' + str(self.score))
