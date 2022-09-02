import pygame
from settings import FIGURES, COLORS


class Figure:
    def __init__(self, figure: int):
        self.figure = figure
        self.color = COLORS[figure]
        self.figure_map = FIGURES[figure]

    def set_figure(self, figure: int):
        self.figure = figure
        self.color = COLORS[figure]
        self.figure_map = FIGURES[figure]

    def set_figure_map(self, figure_map: tuple):
        self.figure_map = figure_map

    def get_color(self) -> tuple[int, int, int]:
        return self.color

    def get_color_index(self) -> int:
        return self.figure

    def get_map(self) -> tuple:
        return self.figure_map

    def rotated_figure(self) -> tuple:
        return tuple([(-self.figure_map[i][1], self.figure_map[i][0]) for i in range(4)])


class Button(pygame.sprite.Sprite):
    def __init__(self, pos: tuple[int, int], size: tuple[int, int], text: str, color=(0, 0, 0), bg_color=(0, 0, 0),
                 hovered_color=(0, 0, 0), fontsize=45, option=0, *groups):
        super().__init__(*groups)
        self.image = pygame.surface.Surface(size, pygame.SRCALPHA, 32)
        self.pos = pos
        self.rect = self.image.get_rect(topleft=pos)
        self.text = text
        self.color = color
        self.bg_color = bg_color
        self.hovered_color = hovered_color
        self.fontsize = fontsize
        self.is_hovered = False
        self.option = option

    def update(self) -> None:
        self.image.fill(self.hovered_color if self.is_hovered else self.bg_color)
        font = pygame.font.Font(None, self.fontsize)
        text = font.render(self.text, True, self.color)
        self.image.blit(text, (self.rect.width // 2 - text.get_width() // 2,
                               self.rect.height // 2 - text.get_height() // 2))
        if self.is_hovered:
            self.unhover()

    def hover(self):
        self.is_hovered = True

    def unhover(self):
        self.is_hovered = False

    def get_option(self) -> int:
        return self.option


class TextObject:
    def __init__(self, text: str, screen: pygame.surface.Surface, font=None, font_size=72, color=(0, 0, 0)):
        self.text = text
        self.screen = screen
        self.font = font
        self.font_size = font_size
        self.color = color
        self.update_elements()

    def update_elements(self):
        self.font_element = pygame.font.Font(self.font, self.font_size)
        self.text_element = self.font_element.render(self.text, True, self.color)

    def get_width(self) -> int:
        return self.text_element.get_width()

    def get_height(self) -> int:
        return self.text_element.get_height()

    def change_color(self, color=(0, 0, 0)):
        self.color = color
        self.update_elements()

    def change_text(self, text: str):
        self.text = text
        self.update_elements()

    def render(self, pos: tuple[int, int]):
        self.screen.blit(self.text_element, pos)