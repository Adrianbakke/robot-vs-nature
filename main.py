from gamemanager import GameManager
import pygame

pygame.init()


if __name__ == "__main__":
    print("Creating game object...")
    gm = GameManager()
    print("Done. Starting run method")
    gm.start_screen()
    gm.game()
