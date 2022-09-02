import pygame
import sys
from settings import game_state, GameState, OPTION_LIST


def check_buttons_input(group: pygame.sprite.Group):
    for el in group:
        if el.rect.collidepoint(pygame.mouse.get_pos()):
            el.hover()
            if any(pygame.mouse.get_pressed()):
                eval(f"{OPTION_LIST[el.get_option()]}()")


def start_game():
    game_state.set_state(GameState.playing.value)


def terminate():
    pygame.quit()
    sys.exit()