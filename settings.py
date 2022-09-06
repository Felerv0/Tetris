from userInput import UserInput
from enum import Enum

# game consts
COLORS = [(0, 0, 0), (0, 255, 255), (255, 255, 0), (255, 0, 0),
          (0, 255, 0), (255, 128, 0), (0, 128, 255), (255, 0, 255)]

OPTION_LIST = ["terminate", "start_game", "open_settings", "game.pause", "game.restart_game"]

FIGURES = [((0, 0), (0, 0), (0, 0), (0, 0)),
           ((0, 0), (1, 0), (0, 1), (1, 1)),
           ((0, -1), (0, 0), (0, 1), (0, 2)),
           ((0, -1), (0, 0), (1, 0), (1, 1)),
           ((0, -1), (0, 0), (-1, 0), (-1, 1)),
           ((-1, -1), (0, -1), (0, 0), (0, 1)),
           ((1, -1), (0, -1), (0, 0), (0, 1)),
           ((-1, 0), (0, 0), (1, 0), (0, 1))]
# colors
BORDER_COLOR = (50, 50, 50)
BACKGROUND_COLOR = (0, 0, 0)
# sizes
OFFSET_Y = 2
FPS = 60
CELL_SIZE = 35
BORER_SIZE = 1
field_size = (10, 19)
screen_size = (screen_width, screen_height) = (CELL_SIZE * field_size[0],
                                               CELL_SIZE * field_size[1])
FIGURES_COUNT = len(FIGURES)
# getting input
getInput = UserInput()


# classes
class GlobalGameState:
    def __init__(self):
        self.game_state = 0

    def __eq__(self, other: int) -> bool:
        return self.game_state == other

    def set_state(self, state):
        self.game_state = state

game_state = GlobalGameState()


class GameState(Enum):
    menu = 0
    playing = 1


class Options(Enum):
    quit = 0
    play = 1
    settings = 2
    resume = 3
    restart = 4


class Color(Enum):
    black = 0
    blue = 1
    yellow = 2
    red = 3
    green = 4
    orange = 5
    dark_blue = 6
    pink = 7


class Types(Enum):
    none = 0
    o = 1
    i = 2
    s = 3
    z = 4
    l = 5
    j = 6
    t = 7
