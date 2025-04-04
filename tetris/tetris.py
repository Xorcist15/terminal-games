from blessed import Terminal
import time
import copy
from tetrimino import Tetrimino as Tet

term = Terminal()

FPS = 0.5     # 2 frames rendered per second  
WIDTH = 10
HEIGHT = 20

game_paused = False

grid = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]

# debugging functions
def debugger(msg, x, y):
    print(term.move_xy(x, y) + msg)
    return

def render_grid_state():
    for i in range(len(grid)):  
        for j in range(len(grid[0])):
            if grid[i][j]:
                j*=2
                print(term.move_xy(j + 60, i) + term.green("1"))
            else:
                j*=2
                print(term.move_xy(j + 60, i) + term.red("0"))
    return

def graduations():
    # vertical
    for i in range(len(grid)):
        print(term.move_xy(22, i) + str(i))
    # horizontal
    for i in range(len(grid[0])):
        print(term.move_xy(i * 2, 22) + str(i))
    return

def pause_game():
    global game_paused
    game_paused = not game_paused 
    msg = term.blue("GAME PAUSED    ")
    if not game_paused:
        msg = term.green("GAME NOT PAUSED")
    debugger(msg, 30, 16)
    return

def render_grid():
    #print(term.clear())
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
    for i in range(len(piece.shape)): 
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j]:
                # simulate next move
                next_x = piece.x + j + dx
                next_y = piece.y + i + dy
                if next_x < 0 or next_x >= WIDTH or next_y < 0 or next_y >= HEIGHT:
                    return False
                if grid[next_y][next_x]:
                    return False
    return True

def is_valid_rotation(piece):
    clone = copy.deepcopy(piece)    
    # simulate rotation
    clone.rotate()
    for i in range(len(clone.shape)):
        for j in range(len(clone.shape[0])):
            if clone.shape[i][j]:
                new_x = clone.x + j
                new_y = clone.y + i
                msg = f"new rotation: ({str(new_x)},{str(new_y)})"
                debugger(msg, 30, 5)
                if new_x < 0 or new_x >= WIDTH or new_y < 0 or new_y >= HEIGHT:
                    return False
                if grid[new_y][new_x]:
                    return False
    return True

def check_lines():
    # possible optim, count backwards
    for i in range(len(grid)):
        line_complete = True
        for j in range(len(grid[0])):
            if not grid[i][j]:
                line_complete = False
                break
        if(line_complete):
            empty_line(i)
            shift_downwards(i)
    return

def empty_line(index):
    for i in range(len(grid[0])):
        grid[index][i] = None
    return

def shift_downwards(index):
    for i in range(index, 0, -1): 
        for j in range(len(grid[0])):
            grid[i][j] = grid[i - 1][j]
    for i in range(len(grid[0])):
        grid[0][i] = None
    return

def check_game_end(piece):
    for i in range(len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j]:
                pos_x = piece.x + j
                pos_y = piece.y + i
                # something in the way... hmmmmmmmmmmm
                if grid[pos_y][pos_x]:
                    show_end_msg()
    return

def show_end_msg():
    pause_game()
    msg = term.red("YOU LOST")
    debugger(msg, 30, 10)
    return

def place_piece(piece):
    while is_valid_move(piece, 0, 1):
        piece.move(0, 1)
    save_to_grid(piece) 
    return

def save_to_grid(piece):
    for i in range(len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j]:
                pos_x = piece.x + j
                pos_y = piece.y + i
                grid[pos_y][pos_x] = piece.color
                msg = f"saved position: ({str(pos_x)},{str(pos_y)})"
                debugger(msg, 30, 4)
    return

with term.cbreak(), term.fullscreen(), term.hidden_cursor():
    init_time = time.monotonic()
    current_piece = Tet.random_tetrimino()

    # game loop
    while True:
        key = term.inkey(timeout = 0.1)
        if not game_paused:
            # controller hjkli
            if key == 'h':
                # go left
                if is_valid_move(current_piece, -1, 0):
                    current_piece.move(-1, 0)
            elif key == 'j':
                # go down
                if is_valid_move(current_piece, 0, 1):
                    current_piece.move(0, 1)
            elif key == 'k':
                # rotation
                if is_valid_rotation(current_piece):
                    current_piece.rotate()
            elif key == 'l':
                # go right 
                if is_valid_move(current_piece, 1, 0):
                    current_piece.move(1, 0)
            elif key == ' ':
                # place down piece
                place_piece(current_piece)
            elif key == 'q':
                # exit game
                exit()
        if key == 'p':
            pause_game()

        if not game_paused:
            current_time = time.monotonic()
            if current_time - init_time > FPS:
                init_time = time.monotonic()
                # game logic
                if is_piece_placed(current_piece):
                    save_to_grid(current_piece) 
                    current_piece = Tet.random_tetrimino()
                    check_game_end(current_piece)

                # update game state
                current_piece.move(0, 1)
                check_lines()

                # render game state
                render_grid()
                render_piece(current_piece)
                graduations()
                render_grid_state()
