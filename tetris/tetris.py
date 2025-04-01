import time
from blessed import Terminal
from tetrimino import Tetrimino

# Initialize the terminal
term = Terminal()

WIDTH = 10
HEIGHT = 20
FALL_SPEED = 0.5  # Seconds per automatic drop

# None is similar to Null, if there is color than it's not empty
grid = [[None for _ in range(WIDTH)] for _ in range(HEIGHT)]


def render_grid(active_piece):
    print(term.clear())

    # Render grid with stored colors
    for i in range(HEIGHT):
        for j in range(WIDTH):
            if grid[i][j]:  # If a block exists, use its stored color
                print(term.move_xy(j * 2, i) + grid[i][j]("██"), end="")
            else:
                print(term.move_xy(j * 2, i) + ".", end="")

    # Render the active piece
    for i, row in enumerate(active_piece.shape):
        for j, cell in enumerate(row):
            if cell:
                print(term.move_xy((active_piece.x + j) * 2, active_piece.y + i) + active_piece.color("██"), end="")

    print(term.move_xy(0, HEIGHT))  # Move cursor down after rendering


def is_valid_move(piece, dx, dy):
    """Check if moving the piece by (dx, dy) would cause a collision."""
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                new_x = piece.x + j + dx
                new_y = piece.y + i + dy

                # Out of bounds or collision check
                if new_x < 0 or new_x >= WIDTH or new_y >= HEIGHT or grid[new_y][new_x] is not None:
                    return False
    return True


def place_piece(piece):
    """Lock the piece into the grid with its color."""
    for i, row in enumerate(piece.shape):
        for j, cell in enumerate(row):
            if cell:
                grid[piece.y + i][piece.x + j] = piece.color  # Store the color

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    active_piece = Tetrimino.random_tetrimino()
    last_fall_time = time.time()

    while True:
        render_grid(active_piece)
        key = term.inkey(timeout=0.05)

        # Handle user input
        if key == 'q':  # Quit
            break
        elif key == 'h' and is_valid_move(active_piece, -1, 0):  # Move left
            active_piece.move(-1, 0)
        elif key == 'l' and is_valid_move(active_piece, 1, 0):  # Move right
            active_piece.move(1, 0)
        elif key == 'j':  # Instant drop
            while is_valid_move(active_piece, 0, 1):
                active_piece.move(0, 1)
            place_piece(active_piece)
            active_piece = Tetrimino.random_tetrimino()
        elif key == 'k':  # Rotate
            active_piece.rotate()
            if not is_valid_move(active_piece, 0, 0):
                active_piece.rotate()  # Undo rotation if invalid

        # **Automatic downward movement**
        if time.time() - last_fall_time > FALL_SPEED:
            if is_valid_move(active_piece, 0, 1):
                active_piece.move(0, 1)
            else:
                place_piece(active_piece)
                active_piece = Tetrimino.random_tetrimino()
            last_fall_time = time.time()

