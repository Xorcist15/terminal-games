from blessed import Terminal
import time
import copy
from tetrimino import Tetrimino as Tet

term = Terminal()

WIDTH = 10
HEIGHT = 20

game_paused = False

grid = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]

# TODO score system, improve UI, reduce render frequency
# TODO better gameplay mechanics

# debugging functions
def debugger(msg, x, y):
    print(term.move_xy(x, y) + msg)
    return

def render_grid_state():
    screen = ""

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            x = j * 2 + 60  # move right to show the state next to the game
            y = i
            if grid[i][j]:
                screen += term.move_xy(x, y) + term.green("1")
            else:
                screen += term.move_xy(x, y) + term.red("0")

    print(screen)

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


def render_grid(piece):
    screen = ""

    # Render the static grid first
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            x = j * 2
            y = i
            if grid[i][j]:
                screen += term.move_xy(x, y) + grid[i][j]("1")
            else:
                screen += term.move_xy(x, y) + "."

    positions = []

    # Render the current falling piece
    for i in range(len(piece.shape)):
        for j in range(len(piece.shape[0])):
            if piece.shape[i][j]:
                x = piece.x + j
                y = piece.y + i
                screen += term.move_xy(x * 2, y) + piece.color("1")
                positions.append((x, y))

    # Add debug info
    msg = f"{positions}"
    screen += term.move_xy(20, 20) + msg

    # Clear screen and print everything at once
    print(screen)

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


FALL_FREQUENCY = 0.5
INPUT_FREQUENCY = 0.01

with term.cbreak(), term.fullscreen(), term.hidden_cursor():
    current_piece = Tet.random_tetrimino()

    gravity_timer = time.monotonic()
    input_timer = time.monotonic()

    graduations()

    while True:
        current_time = time.monotonic()

        # input handling 
        if current_time - input_timer >= INPUT_FREQUENCY:
            key = term.inkey(timeout=0)

            if not game_paused:
                if key == 'h' and is_valid_move(current_piece, -1, 0):
                    current_piece.move(-1, 0)
                elif key == 'l' and is_valid_move(current_piece, 1, 0):
                    current_piece.move(1, 0)
                elif key == 'j' and is_valid_move(current_piece, 0, 1):
                    current_piece.move(0, 1)
                elif key == 'k' and is_valid_rotation(current_piece):
                    current_piece.rotate()
                elif key == ' ':
                    if check_game_end(current_piece):  # add this!
                        show_end_msg()
                        break
                    place_piece(current_piece)
                    check_lines()
                    current_piece = Tet.random_tetrimino()
                elif key == 'q':
                    exit()

            if key == 'p':
                pause_game()

            # the problem here is that it's actually alterning between the 2 characters
            # meaning it's switching so fast which creates an unpleasant visual effect
            render_grid(current_piece)
            render_grid_state()

            input_timer = current_time

            # gravity update (FIXED)
        if not game_paused and (current_time - gravity_timer >= FALL_FREQUENCY):
            if is_piece_placed(current_piece):
                # Check if placing the piece would cause game over
                if check_game_end(current_piece):
                    show_end_msg()
                    break  # stop the game loop
                save_to_grid(current_piece)
                check_lines()
                current_piece = Tet.random_tetrimino()
            else:
                current_piece.move(0, 1)
            gravity_timer = current_time


