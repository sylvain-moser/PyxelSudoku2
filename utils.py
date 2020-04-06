import random


def generate_random_puzzle():
    pass


def get_board_spot(mouse_x, mouse_y):
    return min(int(mouse_x // 17), 8), min(int(mouse_y // 17), 8)


def board_is_full(board):
    for row in board:
        for val in row:
            if val == 0:
                return False
    else:
        return True


def format_board(current_board):
    return """
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
---------------------
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
---------------------
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
{} {} {} | {} {} {} | {} {} {}
""".format(
        *[val if val else " " for row in current_board for val in row]
    )


def fill_board(puzzle):
    spots = iter(puzzle)
    puzzle_board = [[int(next(spots)) for _ in range(9)] for _ in range(9)]
    return puzzle_board  # change from a string to a list of list of ints


def read_line_from_puzzlefile(file):
    # Read sudoku data
    f = open(file)
    text = f.read()
    # Get one of the puzzles and its corresponding solution
    lines = text.splitlines()
    line_number = random.randint(0, len(lines))
    return lines[line_number]


def format_puzzle(line):
    line = line.strip()
    puzzle, solution = line.split(",")
    return puzzle, solution