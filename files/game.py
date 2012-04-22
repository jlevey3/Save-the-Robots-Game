import pygame

from app import Application
from main import Instruction

def main():
    # initialize pygame
    pygame.init()
    pygame.display.set_mode((800, 600))

    # create game
    app = Application(Instruction)
    try:
        app.run()
    except KeyboardInterrupt:
        app.quit()

if __name__ == "__main__":
    main()
