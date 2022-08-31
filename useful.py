import pygame
import sys
from settings import game_state, GameState


def start_game():
    game_state.set_state(GameState.playing.value)


def terminate():
    pygame.quit()
    sys.exit()