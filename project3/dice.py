import random
import time
import sys
import os
from itertools import cycle

# ASCII dice faces
DICE_FACES = [
    ["┌─────────┐", "│         │", "│    ●    │", "│         │", "└─────────┘"],
    ["┌─────────┐", "│ ●       │", "│         │", "│       ● │", "└─────────┘"],
    ["┌─────────┐", "│ ●       │", "│    ●    │", "│       ● │", "└─────────┘"],
    ["┌─────────┐", "│ ●     ● │", "│         │", "│ ●     ● │", "└─────────┘"],
    ["┌─────────┐", "│ ●     ● │", "│    ●    │", "│ ●     ● │", "└─────────┘"],
    ["┌─────────┐", "│ ●     ● │", "│ ●     ● │", "│ ●     ● │", "└─────────┘"]
]

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_key_press():
    """Check if 'q' was pressed (non-blocking)"""
    if os.name == 'nt':  # Windows
        import msvcrt
        return msvcrt.kbhit() and msvcrt.getch() == b'q'
    else:  # Linux/Mac
        import tty, termios, sys
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            return sys.stdin.read(1) == 'q'
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

def roll_dice():
    clear_screen()
    print("Rolling... (Press 'q' to stop)")
    
    spinning = cycle(DICE_FACES)
    start_time = time.time()
    
    while time.time() - start_time < 3:  # Max 3 sec animation
        if get_key_press():
            break
        
        # Show current face
        for line in next(spinning):
            print(line)
        
        time.sleep(0.1)
        clear_screen()
    
    result = random.randint(1, 6)
    return result

def main():
    clear_screen()
    print("🎲 Press ENTER to roll ('q' to quit) 🎲")
    
    while True:
        # Wait for Enter or 'q'
        user_input = input()
        if user_input.lower() == 'q':
            print("Goodbye!")
            break
        
        # Roll and show result
        result = roll_dice()
        clear_screen()
        print(f"Result: {result}\n")
        for line in DICE_FACES[result-1]:
            print(line)
        
        print("\nPress ENTER to roll again (ctrl c to quit)")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGoodbye!")