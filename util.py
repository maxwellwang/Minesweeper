def generate_board(d, n):
    """
    Generates a random d x d board containing n mines. Each cell will be a dictionary keeping track of:
    1. whether or not it is a mine or safe (or currently covered)
    2. if safe, the number of mines surrounding it indicated by the clue
    3. the number of safe squares identified around it
    4. the number of mines identified around it
    5. the number of hidden squares around it

    :param d: dimension of board
    :param n: number of mines
    :return: d x d board containing n mines
    """
    board = [[{} for _ in range(d)] for _ in range(d)]
    return board
