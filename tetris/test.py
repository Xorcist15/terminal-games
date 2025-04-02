from blessed import Terminal
import time
from tetrimino import Tetrimino
            
term = Terminal()

# init grid
grid = [[None for _ in range(10)] for _ in range(20)]

WIDTH = 10
HEIGHT = 20
FALL_SPEED = 0.1

def render_grid(piece):
    print(term.clear()) 
    # render grid
    for i in range(HEIGHT): 
        for j in range(WIDTH):
            if grid[i][j]:
                print(term.move_xy(j*2, i) + grid[i][j]("1"), end="")
            else:
                print(term.move_xy(j*2, i) + "0", end="")
    # render current current_piece
    for i in range (len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j] == 1:
                print(term.move_xy((piece.x + j) * 2, piece.y + i) + piece.color("1"))
    return

def is_valid_move(piece, dx, dy):
    if (piece.x + dx < 0 or piece.x + dx + len(piece.shape[0]) > WIDTH):
        return False
    if piece.y + dy < 0 or piece.y + dy + len(piece.shape) > HEIGHT:
        return False
    return True

def is_valid_rotation(piece):


    for i in range(len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j] == 1:
                new_x = piece.x + j
                new_y = piece.y + i
                if grid[new_x][new_y]:
                    return False
    return True

def is_piece_placed(piece):
    for i in range (len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j] == 1:
                new_x = piece.x + j
                new_y = piece.y + i + 1
                if new_y >= HEIGHT:
                    return True
                if grid[new_x][new_y]:
                    return True
    return False

def save_to_grid(piece):
    for i in range (len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j] == 1:
                pos_x = piece.x + j
                pos_y = piece.y + i
                grid[pos_y][pos_x] = piece.color
    return

def place_piece(piece):
    print("hello world")
    

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    current_piece = Tetrimino.random_tetrimino()

    while True:
        render_grid(current_piece)
        time.sleep(FALL_SPEED)

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
                print("hello world")
               # current_piece.rotate()

        elif key == 'space':
            # todo right place piece fn
            print("place piece")

        # if no key press at all, go downwards
        current_piece.move(0, 1)

    
        if(is_piece_placed(current_piece)):
            save_to_grid(current_piece)
            current_piece = Tetrimino.random_tetrimino()

