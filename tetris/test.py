from blessed import Terminal
from tetrimino import Tetrimino
import time

term = Terminal()

GRID_RENDER_FREQUENCY = 0.5
HEIGHT = 20
WIDTH = 10
grid = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]

def render_grid():
    # clear terminal
    print(term.clear())  # Clear screen before rendering
    # top
    grid_str = term.move_xy(0, 0) + "╔" + "═" * (WIDTH * 2) + "╗\n"
    # body
    for i in range(len(grid)):
        row = "║"
        for j in range(len(grid[0])):
            cell = grid[i][j]("██") if grid[i][j] else "░░"
            row += cell
            if j == WIDTH - 1:
                row += "║\n"
        grid_str += row
        grid_str += term.move_xy(0, i + 1) + row
    # bottom
    grid_str += term.move_xy(0, HEIGHT + 1) + "╚" + "═" * (WIDTH * 2) + "╝"
    # print grid
    print(grid_str)  
    return

def render_piece(piece):
    for i in range(len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j]:
                print(term.move_xy((piece.x + j * 2) + 1, piece.y + i + 1) + piece.color("██"))
    return

def is_piece_placed(piece):
    # rows
    for i in range(len(piece.shape)):
        # cells
        for j in range(len(piece.shape[0])):
            # if cell
            if piece.shape[i][j]:
                # simulate drop by one
                new_x = piece.x + j
                new_y = piece.y + i + 1
                # reaching bottom
                if new_y >= HEIGHT:
                    return True
                # collision w/ other pieces
                if grid[new_y][new_x]:
                    return True
    return False

def save_to_grid(piece):
    for i in range(len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j]:
                pos_x = 1 + piece.x + j
                pos_y = 1 + piece.y + i
                grid[pos_x][pos_y] = piece.color
    return

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    # init stuff for game
    init_time = time.monotonic()

    current_piece = Tetrimino.random_tetrimino()
    while True:
        # game loop 
        time.sleep(0.1)
        passed_time = time.monotonic()

        if is_piece_placed(current_piece):
            current_piece = Tetrimino.random_tetrimino()

        if passed_time - init_time > GRID_RENDER_FREQUENCY:
            init_time = time.monotonic()
            render_grid()
            render_piece(current_piece)
            if not is_piece_placed(current_piece):
                save_to_grid(current_piece)
                current_piece.move(0, 1)



