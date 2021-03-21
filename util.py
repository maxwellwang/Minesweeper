from random import randrange
import sympy


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
    if len(mines) == 0:
        return 1
    return num_correctly_flagged_mines / len(mines)


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
        # print_board(self.board)
        # print('Score: ' + str(self.score))


class Info:
    # This class stores information about cells we know are safe or mined
    def __init__(self, mines=None, safe=None):
        if safe is None:
            safe = set()
        if mines is None:
            mines = set()
        self.mines = mines
        self.safe = safe

    def __repr__(self):
        return "Mines: " + ' '.join(str(mine) for mine in self.mines) + "\n" + "Safe: " + ' '.join(
            str(s) for s in self.safe)

    def combine(self, info):
        """
        Combines self with another set of information and checks for inconsistencies
        :param info: Another Info object
        :return: Nothing
        """
        if len(info.mines) + len(info.safe) != len(info.mines.union(info.safe)):
            raise Exception("Some cells are both safe and mines!")
        if len(self.mines.intersection(info.safe)) != 0:
            raise Exception("Clue conflict 1")
        if len(self.safe.intersection(info.mines)) != 0:
            raise Exception("Clue conflict 2")
        self.mines = self.mines.union(info.mines)
        self.safe = self.safe.union(info.safe)

    def has_new(self):
        """
        Checks if there is new information that can be used
        :return: True if so, False otherwise
        """
        return len(self.mines) != 0 or len(self.safe) != 0


class ClueSolver:
    # Clue represents the information around a single cell with a number
    class Clue:
        def __init__(self, num_mines, hidden_cells, mined_cells):
            self.num_mines = num_mines - mined_cells
            self.hidden_cells = hidden_cells

        def gen_row(self, dim):
            """
            Generates the row representation of the equation a clue represents of the form
            (sum a_{i * dim + j} = b) where a is 1 if cell (i, j) is hidden, 0 o/w, b is clue value
            :param dim: Dimension of the board
            :return: The row representing the equation
            """
            row = [0] * (dim * dim + 1)
            for cell in self.hidden_cells:
                row[cell[0] * dim + cell[1]] = 1
            row[-1] = self.num_mines
            return row

        def solve(self):
            """
            Solves a clue.
            If the number of mines is the same as the number of hidden cells, all cells must be mines
            If the number of mines is zero, all cells must be safe
            Otherwise, there is no new information
            :return: an Info object containing any new information
            """
            if self.num_mines == len(self.hidden_cells):
                return Info(mines=self.hidden_cells)
            elif self.num_mines == 0:
                return Info(safe=self.hidden_cells)
            else:
                return Info()

    def __init__(self, dim, info):
        self.clues = []
        self.dim = dim
        self.dense_to_sparse = {}
        self.selection = info[1]

    def index_to_cell(self, index):
        """
        Converts an index in the array to
        :param index: The index of the particular cell in the row
        :return: The cell
        """
        return index // self.dim, index % self.dim

    def add_clue(self, num_mines, hidden_cells, mined_cells):
        """
        Given the number of mines, hidden cells, and mined cells, adds clue to list of clues
        :param num_mines: The clue number (how many mines are around it)
        :param hidden_cells: Number of hidden cells around clue
        :param mined_cells: Number of mined cells around clue
        :return: Nothing, adds clue to self
        """
        # If there is nothing hidden, we have nothing to learn, so ignore it
        if len(hidden_cells) == 0:
            return
        self.clues.append(self.Clue(num_mines, hidden_cells, mined_cells))

    def get_next_cell(self, sympy_mat):
        """
        For the bonus, picks the next best cell to use
        Once we solve the matrix, we pick the cell included in the MOST number of constraints
        This maximizes the amount of other clues we may be able to solve next
        :param sympy_mat: The RREF'd sympy matrix
        :return: The cell which is in the most number of constraints (equations)
        """
        max_constraint, max_cell = -1, -1
        if self.selection:
            for i in range(sympy_mat.cols - 1):
                if sum(sympy_mat.col(i)) > max_constraint:
                    max_constraint = sum(sympy_mat.col(i))
                    max_cell = i

        return (-1, -1) if max_cell == -1 else self.index_to_cell(self.dense_to_sparse[max_cell])

    def generate_sympy(self):
        """
        Once we have all the clues, we want to combine them all to perform inference
        This method does just that and returns the matrix which represents our knowledge base
        :return: The matrix
        """
        sparse_mat, dense_mat = [], []
        empty_col = [True] * (self.dim * self.dim) + [False]

        # For each clue, add the row form of it to the matrix
        for clue in self.clues:
            sparse_mat.append(clue.gen_row(self.dim))

        # The matrix could be very big, so we make it small by removing all columns with only 0s
        for row in sparse_mat:
            for i, e in enumerate(row):
                if e != 0:
                    empty_col[i] = False

        # Track which column in the dense matrix corresponds to in the sparse matrix for conversion later
        self.dense_to_sparse = {}
        filled_col, cur_col = set(), 0
        for i, e in enumerate(empty_col):
            if not e:
                self.dense_to_sparse[cur_col] = i
                cur_col += 1
                filled_col.add(i)
        filled_col.add(self.dim * self.dim)

        # Generate the dense matrix which has no column with only 0s
        for row in sparse_mat:
            dense_mat.append([e for i, e in enumerate(row) if i in filled_col])

        # RREF matrix to simplify and obtain solutions
        sympy_mat = sympy.Matrix(dense_mat)
        return sympy_mat.rref()[0]

    def solve_basic(self):
        """
        This solves the clues using the basic agent strategy.
        :return: The solution as an Info object storing the new information
        """
        sol = Info()
        for clue in self.clues:
            sol.combine(clue.solve())
        return sol, None

    def solve_improved(self):
        """
        This uses the matrix form of our knowledge base after inference has been performed
        Reverses the compression to the dense matrix, and solves the clues
        :return: The solution, in the form of Info object, as well as the next cell to pick if needed
        """
        sympy_mat = self.generate_sympy()

        # Use solved matrix to check for new information
        sol = Info()
        for sympy_row in sympy_mat.tolist():
            # Expand row back into long form
            row = [0] * (self.dim * self.dim + 1)
            for i, e in enumerate(sympy_row):
                row[self.dense_to_sparse[i]] = e
            # Deduce the clues
            if sum([i for i in row[:-1] if i < 0]) == 0:
                clue = self.Clue(row[-1], set(self.index_to_cell(i) for i, e in enumerate(row[:-1]) if e != 0),
                                 sum([i - 1 for i in row[:-1] if i > 1]))
                sol.combine(clue.solve())

        return sol, self.get_next_cell(sympy_mat)

    def solve(self):
        """
        This attempts to solve the board. First it uses the basic algorithm. If there is no new info, it uses improved.
        :return: The solution and the next cell to pick
        """
        sol, _ = self.solve_basic()
        if sol.has_new():
            return sol, (-1, -1)
        else:
            if False:
                print("Using inference")
            return self.solve_improved()


class ImprovedAgent:
    def __init__(self, arg1, arg2, info):
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
        self.score = 0
        self.dim = len(board)
        self.info = info
        self.viz = len(info) == 3

    def infer(self):
        """
        Iterates through the current board and collects clue to send to the clue solver
        Then, gets the solved clues and updates the board, repeating if needed
        :return: The next cell to pick if needed
        """
        solver = ClueSolver(self.dim, self.info)
        for i in range(self.dim):
            for j in range(self.dim):
                # If the cell is a number, we can generate a clue
                if self.board[i][j].isdigit():
                    hidden_cells = set()
                    mined_cells = 0
                    for pair in get_neighbor_coordinates((i, j), self.dim):
                        cell = self.board[pair[0]][pair[1]]
                        # Count mined cells, add hidden cells to list
                        if cell == 'M' or cell == 'X':
                            mined_cells += 1
                        elif cell == '?':
                            hidden_cells.add(pair)
                        elif not cell.isdigit():
                            raise Exception("Unexpected cell value: " + cell)
                    # Add new clue to the solver
                    solver.add_clue(int(self.board[i][j]), hidden_cells, mined_cells)

        # Bonus: add global information clue
        if self.info[0] != -1:
            hidden_cells = set()
            mined_cells = 0
            for i in range(self.dim):
                for j in range(self.dim):
                    if self.board[i][j] == '?':
                        hidden_cells.add((i, j))
                    if self.board[i][j] == 'M' or self.board[i][j] == 'X':
                        mined_cells += 1
            solver.add_clue(self.info[0], hidden_cells, mined_cells)

        # Solves all clues
        solution, next_cell = solver.solve()
        new_clues = False

        # If we determine cells as mines, mark them as such
        for pair in solution.mines:
            self.board[pair[0]][pair[1]] = 'M'
        # If we determine cells as safe, query them
        for pair in solution.safe:
            self.board = query(pair, self.board, self.mines)

        # If doing play by play, print the board
        if self.viz:
            print("Clues")
            print(solution)
            print_board(self.board)

        # If board has updated, infer again
        if solution.has_new() and not completed(self.board):
            next_cell = self.infer()

        return next_cell

    def run(self):
        """
        Runs improved agent on the minesweeper board, and prints final score.

        :return: nothing
        """
        while not completed(self.board):
            # Infer for as long as we can
            next_cell = self.infer()
            # No new info able to be inferred, query a cell
            if not completed(self.board):
                # reveal random cell and update info
                if not self.info[1] or next_cell == (-1, -1):
                    # Query a random cell
                    self.board, (i, j) = random_query(self.board, self.mines)
                    if self.viz:
                        print("Forced to guess: " + str(i) + " " + str(j))
                        print_board(self.board)
                else:
                    # Bonus: query the cell given by our solver as the best pick
                    query(next_cell, self.board, self.mines)

        self.score = get_score(self.board, self.mines)
        # print('Score: ' + str(self.score))
