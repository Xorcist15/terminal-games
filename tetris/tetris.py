from blessed import Terminal
import time
from tetrimino import Tetrimino as Tet

term = Terminal()

FPS = 0.5     # 10 frames rendered per second  
WIDTH = 10
HEIGHT = 20

grid = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]

def graduations():
    # vertical
    for i in range(len(grid)):
        print(term.move_xy(22, i) + str(i))
    # horizontal
    for i in range(len(grid[0])):
        print(term.move_xy(i * 2, 22) + str(i))
    return

def render_grid():
    print(term.clear())

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]:
                print(term.move_xy(j * 2, i) + grid[i][j]("1"))
            else:
                print(term.move_xy(j * 2, i) + ".")
    return

def render_piece(piece):
    for i in range(len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j]:
                print(term.move_xy((piece.x + j) * 2, piece.y + i) + piece.color("1"))
    return

def is_piece_placed(piece):
    msg = f"current position: ({str(piece.x)},{str(piece.y)})"
    debugger(msg, 30, 2)
    for i in range(len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j]:
                new_x = piece.x + j
                # simulate down by one
                new_y = piece.y + i + 1
                msg = f"new position: ({str(new_x)},{str(new_y)})"
                debugger(msg, 30, 3)
                if new_y >= HEIGHT:
                    return True
                if grid[new_y][new_x]:
                    return True
    return False

def is_valid_move(piece, dx, dy):
    # write this function probab tomorrow
    return True

def debugger(msg, x, y):
    print(term.move_xy(x, y) + msg)
    return

def save_to_grid(piece):
    for i in range(len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j]:
                pos_x = piece.x + j
                pos_y = piece.y + i
                grid[pos_y][pos_x] = piece.color
    msg = f"saved position: ({str(piece.x)},{str(piece.y)})"
    debugger(msg, 30, 4)
    return

with term.cbreak(), term.fullscreen(), term.hidden_cursor():
    init_time = time.monotonic()
    current_piece = Tet.random_tetrimino()

    while True:
        current_time = time.monotonic()
        if current_time - init_time > FPS:
            init_time = time.monotonic()
            render_grid()
            render_piece(current_piece)
            graduations()
            #current_piece.move(0, 1)
            if is_piece_placed(current_piece):
                save_to_grid(current_piece) 
                current_piece = Tet.random_tetrimino()

            # controller hjkli
            key = term.inkey()
            if key == 'h':
                # go left
                current_piece.move(-1, 0)
            elif key == 'j':
                # go down
                current_piece.move(0, 1)
            elif key == 'k':
                # go up
                current_piece.move(0, -1)
            elif key == 'l':
                # go right 
                current_piece.move(1, 0)
            elif key == ' ':
                current_piece.rotate()

