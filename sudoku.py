"""Sudoku Game"""
import random
from copy import deepcopy
import pyxel


def generate_random_puzzle():
    pass


## Check if the board is valid.
def rowsValid(board):
    for row in board:
        if len([val for val in row if val]) == len(
            set(val for val in row if val)
        ):  # check if the values are all unique, not counting zeroes
            continue
        else:
            return False
    return True


def cols_vald(board):
    is_valid = []
    for col in zip(*board):
        is_valid.append(
            len(list(filter(bool, col))) == len(set(filter(bool, col)))
        )  # check if the column contains unique values, not counting zeroes
    if all(is_valid):  # if all the columns are valid
        return True
    else:
        return False


def board_valid(problem_board, solution_board):
    # all the rules of sudoku haven't been broken
    if rowsValid(problem_board):
        if cols_vald(problem_board):
            if True:  # box_valid(problem_board):
                pass
            else:
                return False
        else:
            return False
    else:
        return False

    # the board matches the solution board so far.
    for pcol, scol in zip(problem_board, solution_board):
        for pval, sval in zip(pcol, scol):
            if pval:
                if pval == sval:
                    continue
                else:
                    return False
    return True


def update_board(board, row, col, value):
    new_board = deepcopy(board)
    new_board[row][col] = value
    return new_board


def draw():
    global puzzle_board
    global solution_board
    global is_valid
    global cell_selected
    global selected_value
    global game_won
    if game_won:
        pyxel.cls(10)  # Make bakcground yellow if game is won
    # Draw each space
    for i, row in enumerate(puzzle_board):
        for j, value in enumerate(row):
            x_offset = 2
            y_offset = 2
            x = i * 16 + i + x_offset  # where to put the subimage

            y = j * 16 + j + y_offset  # where to put the subimage
            image_size = 16
            w = image_size

            h = image_size
            u = 0
            v = value * 16
            if cell_selected == (i, j):
                transparent_color = 7
            else:
                transparent_color = 10

            pyxel.blt(
                x, y, 0, u, v, w, h, transparent_color
            )  # copy part of image from resource file to the screen.
    # Draw the lines of the board
    lines_col = 0
    pyxel.rect(0 + x_offset, 50 + y_offset, w=16 * 9 + 8, h=1, col=lines_col)
    pyxel.rect(0 + x_offset, 101 + y_offset, w=16 * 9 + 8, h=1, col=lines_col)
    pyxel.rect(50 + x_offset, 0 + y_offset, h=16 * 9 + 8, w=1, col=lines_col)
    pyxel.rect(101 + x_offset, 0 + y_offset, h=16 * 9 + 8, w=1, col=lines_col)

    pyxel.rect(0, 156, h=7, w=200, col=0)

    for idx in range(9):
        if selected_value == idx + 1:
            transparent_color = 7
        else:
            transparent_color = 10
        pyxel.blt(
            idx * 16 + idx + x_offset,
            165,
            0,
            u=0,
            v=(idx + 1) * 16,
            w=image_size,
            h=image_size,
            colkey=transparent_color,
        )  # copy part of image from resource file to the screen.


def get_board_spot(mouse_x, mouse_y):
    return min(int(mouse_x // 17), 8), min(int(mouse_y // 17), 8)


def update():
    global puzzle_board
    global solution_board
    global is_valid
    global cell_selected
    global selected_value
    global game_won
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

    # select the board spot when the player clicks the left mouse button
    if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON):
        mouse_pos = (pyxel.mouse_x, pyxel.mouse_y)

        board_spot = get_board_spot(*mouse_pos)
        if mouse_pos[1] < 155:
            cell_selected = board_spot
        else:
            selected_value = board_spot[0] + 1

    # update the board spot when the player clicks the right mouse button
    if pyxel.btnp(pyxel.MOUSE_RIGHT_BUTTON):
        mouse_pos = (pyxel.mouse_x, pyxel.mouse_y)

        board_spot = get_board_spot(*mouse_pos)
        x, y = board_spot
        cell_value = puzzle_board[x][y]
        if cell_value != selected_value:
            puzzle_board[x][y] = selected_value
        else:
            puzzle_board[x][y] = 0

    is_valid = board_valid(puzzle_board, solution_board)

    if board_is_full(puzzle_board):

        if board_valid(puzzle_board):

            game_won = True
        else:
            game_won = False
    else:
        game_won = False


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
    return puzzle_board # change from a string to a list of list of ints


def read_line_from_puzzlefile(file):
    ## Read sudoku data
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


game_won = False

line = read_line_from_puzzlefile("sudoku.csv")
puzzle, solution = format_puzzle(line)

## Make a board structure to fill in the data with.
empty_board = [[0 for _ in range(9)] for _ in range(9)]

## Fill Board with puzzle data
puzzle_board = fill_board(puzzle)
solution_board = fill_board(solution)

rowsValid(solution_board)
cols_vald(solution_board)

pyxel.init(156, 183, caption="Sudoku Game")

## change board
selected_value = 1
cell_selected = (0, 0)

update_board(puzzle_board, 4, 4, 8)

pyxel.cls(3)
pyxel.text(1, 1, "8", 0)

is_valid = True
pyxel.load("my_resource.pyxres", True, True)
image = pyxel.image(0)

###start the game###
pyxel.mouse(True)
pyxel.run(update, draw)

print("That was fun, why don't we play again?")
