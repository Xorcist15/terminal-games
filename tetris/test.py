from blessed import Terminal
import time
from tetrimino import Tetrimino

grid = [[None for _ in range(10)] for _ in range(20)]

WIDTH = 10
HEIGHT = 20
FALL_SPEED = 0.5

def render_grid(current_piece):
    print(term.clear()) 

    # render grid
    for i in range(HEIGHT): 
        for j in range(WIDTH):
            print(term.move_xy(j*2, i) + "0", end="")

    # render current current_piece
    for i in range (len(current_piece.shape)):
        for j in range(len(current_piece.shape[0])):
            if current_piece.shape[i][j] == 1:
                print(term.move_xy((current_piece.x + j) * 2, current_piece.y + i) + current_piece.color("1"))

def is_placed(current_piece):
    # todo write some colliison detection
    print("hello world") 


            
term = Terminal()

current_piece = Tetrimino.random_tetrimino()

with term.fullscreen(), term.cbreak(), term.hidden_cursor():
    while True:
        render_grid(current_piece)
        time.sleep(FALL_SPEED)
        current_piece.move(0, 1)

