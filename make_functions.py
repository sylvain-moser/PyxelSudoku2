import pyxel
from board import board_valid

from utils import get_board_spot , board_is_full , format_board, fill_board, read_line_from_puzzlefile, format_puzzle


def make_functions(puzzle_board, solution_board,is_valid, cell_selected, selected_value, game_won):
    def draw():
        nonlocal puzzle_board
        nonlocal solution_board
        nonlocal is_valid
        nonlocal cell_selected
        nonlocal selected_value
        nonlocal game_won
        if game_won:
            pyxel.cls(10)  # Make background yellow if game is won
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


    def update():
        nonlocal puzzle_board
        nonlocal solution_board
        nonlocal is_valid
        nonlocal cell_selected
        nonlocal selected_value
        nonlocal game_won
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

    return update, draw
