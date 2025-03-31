from blessed import Terminal

# Initialize the terminal
term = Terminal()

# Print a simple message
with term.fullscreen(), term.cbreak():
    print(term.move_yx(0, 0) + term.green('Welcome to Tetris!'))
    print(term.move_yx(2, 0) + term.red('Use arrow keys to move, q to quit.'))

    while True:
        # Wait for a key press
        key = term.inkey()

        if key == 'q':  # Quit on 'q'
            break
        elif key == term.KEY_UP:  # Arrow up
            print(term.move_yx(4, 0) + 'Up pressed')
        elif key == term.KEY_DOWN:  # Arrow down
            print(term.move_yx(4, 0) + 'Down pressed')
        elif key == term.KEY_LEFT:  # Arrow left
            print(term.move_yx(4, 0) + 'Left pressed')
        elif key == term.KEY_RIGHT:  # Arrow right
            print(term.move_yx(4, 0) + 'Right pressed')
