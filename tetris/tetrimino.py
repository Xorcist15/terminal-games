from blessed import Terminal
import random

term = Terminal()

TETRIMINOS = {
    "I": ([[1, 1, 1, 1]], term.cyan),
    "O": ([[1, 1], 
           [1, 1]], term.yellow),
    "T": ([[1, 1, 1], 
           [0, 1, 0]], term.magenta),
    "J": ([[1, 0, 0],
           [1, 1, 1]], term.blue),
    "L": ([[0, 0, 1],
           [1, 1, 1]], term.orange),
    "S": ([[0, 1, 1],
           [1, 1, 0]], term.green),
    "Z": ([[1, 1, 0],
           [0, 1, 1]], term.red)
}

class Tetrimino:
    def __init__(self, name, x=4, y=-1):
        self.name = name
        self.shape, self.color = TETRIMINOS[name]
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def rotate(self):
        # rotate the piece
        self.shape =  [list(row) for row in zip(*self.shape[::-1])]

    @staticmethod
    def random_tetrimino():
        name = random.choice(list(TETRIMINOS.keys()))
        return Tetrimino(name)
