import time
import copy
from blessed import Terminal
from tetrimino import Tetrimino
            
term = Terminal()

# init grid
grid = [[None for _ in range(10)] for _ in range(20)]
WIDTH = 10
HEIGHT = 20
FALL_SPEED = 1
score = 0

def render_grid(piece):
    print(term.clear()) 
    # render grid
    for i in range(HEIGHT): 
        for j in range(WIDTH):
            if grid[i][j]:
                print(term.move_xy(j*2, i) + grid[i][j]("██"), end="")
            else:
                print(term.move_xy(j*2, i) + "0", end="")
    # render current current_piece
    for i in range (len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j] == 1:
                print(term.move_xy((piece.x + j) * 2, piece.y + i) + piece.color("██"))
    return

def is_valid_move(piece, dx, dy):
    # line
    for i in range(len(piece.shape)):
        # cell
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j]:
                # simulate next move
                new_x = piece.x + j + dx
                new_y = piece.y + i + dy
                if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
                    return False
                if grid[new_y][new_x]:
                    return False
    return True

def is_valid_rotation(piece):
    # create copy, due to pass by ref
    clone = copy.deepcopy(piece)
    clone.rotate()
    # lines
    for i in range(len(clone.shape)):
        # cells
        for j in range(len(clone.shape[0])):
            # if cell active
            if clone.shape[i][j] == 1:
                # simulate rotation
                new_x = clone.x + j
                new_y = clone.y + i
                # out of bounds collision
                if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
                    return False

                # if collision return false
                if grid[new_y][new_x]:
                    return False
    return True

def is_piece_placed(piece):
    # loop over lines
    for i in range (len(piece.shape)):
        # loop over cells
        for j in range(len(piece.shape[0])):
            # if not null
            if piece.shape[i][j] == 1:
                # simulate next position
                new_x = piece.x + j
                new_y = piece.y + i + 1
                if new_y >= HEIGHT:
                    return True
                if grid[new_y][new_x]:
                    return True
    return False

def save_to_grid(piece):
    for i in range (len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j] == 1:
                pos_x = piece.x + j
                pos_y = piece.y + i
                if 0 <= pos_x < WIDTH and 0 <= pos_y < HEIGHT:
                    grid[pos_y][pos_x] = piece.color
    return

def place_piece(piece):
    while (not is_piece_placed(piece)) :
        piece.move(0, 1)
    save_to_grid(piece)
    return

def check_full_lines():
    for i, line in enumerate(grid):
        line_complete = True
        for cell in line:
            if not cell:
                line_complete = False
                break
        if line_complete:
            # empty the line
            for j in range(len(grid[0])):
                grid[i][j] = None
            # shift downwards by 1
            drop_by_one(i)
    return

def drop_by_one(index):
    for i in range(index, 0, -1):
        for j in range(len(grid[0])):
            grid[i][j] = grid[i - 1][j]
    for i in range(len(grid[0])):
        grid[0][i] = None
    return

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    current_piece = Tetrimino.random_tetrimino()
    last_fall_time = time.monotonic()

    while True:
        render_grid(current_piece)
        check_full_lines()

        key = term.inkey(timeout=0.05)
        
        if key == 'q':
            break

        elif key == 'h':
            # go left
            if is_valid_move(current_piece, -1, 0):
                current_piece.move(-1, 0)

        elif key == 'l':
            # go right
            if is_valid_move(current_piece, 1, 0):
                current_piece.move(1, 0)

        elif key == 'j':
            # go down
            if is_valid_move(current_piece, 0, 1):
                current_piece.move(0, 1)

        elif key == 'k':
            # rotate
            if is_valid_rotation(current_piece):
               current_piece.rotate()

        elif key == ' ':
            # todo right place piece fn
            place_piece(current_piece)

        current_time = time.monotonic()

        if(is_piece_placed(current_piece)):
            save_to_grid(current_piece)
            current_piece = Tetrimino.random_tetrimino()

        if (current_time - last_fall_time > FALL_SPEED):
            current_piece.move(0, 1)
            last_fall_time = current_time 


