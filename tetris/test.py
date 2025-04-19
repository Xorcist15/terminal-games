import os
import time

# ANSI colors
RED = "\033[41m  \033[0m"
BLUE = "\033[44m  \033[0m"
GREEN = "\033[42m  \033[0m"
YELLOW = "\033[43m  \033[0m"
CYAN = "\033[46m  \033[0m"
MAGENTA = "\033[45m  \033[0m"
WHITE = "\033[47m  \033[0m"
RESET = "\033[0m"

def draw_board():
    os.system('clear')  # Use 'cls' on Windows
    print("┌" + "─" * 20 + "┐")
    for _ in range(20):
        print("│" + " " * 20 + "│")
    print("└" + "─" * 20 + "┘")
    
    # Next piece preview
    print("\nNext:")
    print("┌────┐")
    print("│" + RED + RED + "│")
    print("│" + RED + RED + "│")
    print("└────┘")

    # Game info
    print(f"\nScore:  {12345}")
    print(f"Level:  {3}")
    print(f"Lines:  {12}")

draw_board()
