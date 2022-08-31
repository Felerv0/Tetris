import pygame
from settings import *
from game import *
from useful import *

pygame.init()
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()
pygame.key.set_repeat(280, 125)

tetris = Game(screen, field_size)
menu = Menu(screen)

while True:
    getInput.update()
    if getInput.is_terminated():
        terminate()
    if game_state == GameState.menu.value:
        menu.update()
    elif game_state == GameState.playing.value:
        tetris.update()
    pygame.display.update()
    clock.tick(FPS)