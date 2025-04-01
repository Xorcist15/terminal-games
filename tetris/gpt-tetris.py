from blessed import Terminal
import random, time

term = Terminal()
WIDTH, HEIGHT = 10, 20
SHAPES = [
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # O
    [(0, 0), (-1, 0), (1, 0), (2, 0)],  # I
    [(0, 0), (1, 0), (0, 1), (-1, 1)],  # Z
    [(0, 0), (-1, 0), (0, 1), (1, 1)],  # S
    [(0, 0), (-1, 0), (1, 0), (0, 1)],  # T
    [(0, 0), (1, 0), (2, 0), (2, 1)],  # L
    [(0, 0), (-1, 0), (-2, 0), (-2, 1)]  # J
]

# Grid setup
grid = [[' ' for _ in range(WIDTH)] for _ in range(HEIGHT)]
piece = {"shape": random.choice(SHAPES), "x": WIDTH // 2, "y": 0}

def draw():
    """ Draws the game grid and the current piece """
    print(term.clear)
    temp_grid = [row[:] for row in grid]  # Copy grid

    # Draw current piece
    for dx, dy in piece["shape"]:
        x, y = piece["x"] + dx, piece["y"] + dy
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            temp_grid[y][x] = "#"

    # Render
    for y, row in enumerate(temp_grid):
        print(term.move_yx(y, 0) + "|" + "".join(row) + "|")
    print(term.move_yx(HEIGHT, 0) + "+" + "-" * WIDTH + "+")

def collides(dx, dy):
    """ Checks if the piece collides at the next position """
    for px, py in piece["shape"]:
        x, y = piece["x"] + px + dx, piece["y"] + py + dy
        if y >= HEIGHT or x < 0 or x >= WIDTH or (y >= 0 and grid[y][x] != ' '):
            return True
    return False

def place_piece():
    """ Locks the current piece and spawns a new one """
    for dx, dy in piece["shape"]:
        grid[piece["y"] + dy][piece["x"] + dx] = "#"
    piece.update({"shape": random.choice(SHAPES), "x": WIDTH // 2, "y": 0})

def move(dx, dy):
    """ Moves the piece if no collision """
    if not collides(dx, dy):
        piece["x"] += dx
        piece["y"] += dy
    elif dy:  # If collision while moving down, place piece
        place_piece()

# Game loop
with term.cbreak(), term.hidden_cursor():
    while True:
        draw()
        key = term.inkey(timeout=0.1)  # Non-blocking input

        if key == "q": break
        elif key == term.KEY_LEFT: move(-1, 0)
        elif key == term.KEY_RIGHT: move(1, 0)
        elif key == term.KEY_DOWN: move(0, 1)

        move(0, 1)  # Auto-drop every loop
        time.sleep(0.2)  # Control speed
