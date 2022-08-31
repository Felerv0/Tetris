import pygame
from settings import CELL_SIZE, FIGURES_COUNT, COLORS, BORER_SIZE, BORDER_COLOR, FIGURES, getInput, Types, OFFSET_Y,\
    screen_size, GameState, game_state, Options, OPTION_LIST
from random import randrange
from objects import Figure, Button
from useful import start_game, terminate


class Game:
    def __init__(self, screen, field_size: tuple[int, int]):
        self.screen = screen
        pygame.time.set_timer(pygame.USEREVENT, 400)
        self.is_paused = False

        self.field_size = field_size[0], field_size[1] + OFFSET_Y
        self.field = [[0 for __ in range(field_size[0])] for _ in range(field_size[1] + OFFSET_Y)]
        self.coords = [field_size[0] // 2, 1]
        self.current_figure = Figure(randrange(1, FIGURES_COUNT))
        self.next_figure = Figure(randrange(1, FIGURES_COUNT))

        self.score = 0

    def move_down(self):
        self.coords[1] += 1
        figure = self.current_figure.get_map()
        if not all([0 <= self.coords[1] + figure[i][1] < self.field_size[1] for i in range(4)]):
            self.new_figure(figure)
            return
        if not all([self.field[self.coords[1] + figure[i][1]][self.coords[0] + figure[i][0]] == 0 for i in range(4)]):
            self.new_figure(figure)
        self.check_lines()

    def new_figure(self, figure):
        self.check_lines()
        for i in range(4):
            self.field[self.coords[1] + figure[i][1] - 1][self.coords[0] + figure[i][0]] = self.current_figure.get_color_index()
        self.coords = [self.field_size[0] // 2, 1]
        self.current_figure = self.next_figure
        self.next_figure = Figure(randrange(1, FIGURES_COUNT))

    def horizontal_move(self, n: int):
        if self.check_horizontal_borders(self.coords[0] + n, self.current_figure.get_map()):
            if all([self.field[self.coords[1] + self.current_figure.get_map()[i][1]]
                    [self.coords[0] + n + self.current_figure.get_map()[i][0]] == 0 for i in range(4)]):
                self.coords[0] += n

    def rotate_figure(self):
        if self.current_figure.figure == Types.o.value:
            return
        rotated = self.current_figure.rotated_figure()
        for x_offset in (0, 1, -1, 2, -2):  # смещение, если фигура упёрлась в другую фигуру или стенку
            if self.check_horizontal_borders(self.coords[0] + x_offset, rotated)\
                    and self.check_vertical_borders(self.coords[1], rotated):
                if all([self.field[self.coords[1] + rotated[i][1]]
                        [self.coords[0] + x_offset + rotated[i][0]] == 0 for i in range(4)]):
                    self.current_figure.set_figure_map(self.current_figure.rotated_figure())
                    self.coords[0] += x_offset
                    return

    def drop_figure(self):
        while self.coords != [self.field_size[0] // 2, 1]:
            self.move_down()

    def check_lines(self):
        self.check_loss()
        for i in range(self.field_size[1]):
            if all([self.field[i][j] != 0 for j in range(self.field_size[0])]):
                self.remove_line(i)

    def remove_line(self, index):
        for i in range(index, 0, -1):
            self.field[i] = [el for el in self.field[i - 1]]

    def check_loss(self):
        if any([i != 0 for i in self.field[0] + self.field[1]]):
            print('LOSS')

    def render(self):
        self.screen.fill((0, 0, 0))
        for y in range(OFFSET_Y, self.field_size[1]):
            for x in range(self.field_size[0]):
                rect = pygame.rect.Rect(x * CELL_SIZE, (y - OFFSET_Y) * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, BORDER_COLOR, rect, BORER_SIZE)
                pygame.draw.rect(self.screen, COLORS[self.field[y][x]], rect.inflate(-2 * BORER_SIZE, -2 * BORER_SIZE))
        for i in range(4):
            rect = pygame.rect.Rect((self.coords[0] + self.current_figure.get_map()[i][0]) * CELL_SIZE,
                                    (self.coords[1] + self.current_figure.get_map()[i][1] - OFFSET_Y) * CELL_SIZE,
                                    CELL_SIZE, CELL_SIZE)
            self.screen.fill(self.current_figure.get_color(), rect.inflate(-2 * BORER_SIZE, -2 * BORER_SIZE))

    def check_horizontal_borders(self, x: int, figure: tuple[tuple[int, int]]) -> bool:
        return all([0 <= x + figure[i][0] < self.field_size[0] for i in range(4)])

    def check_vertical_borders(self, y: int, figure: tuple[tuple[int, int]]) -> bool:
        return all([0 <= y + figure[i][0] < self.field_size[1] for i in range(4)])

    def check_input(self):
        if getInput.isKeyDown(pygame.K_ESCAPE):
            self.pause()
        elif getInput.isKeyDown(pygame.K_r):
            self.__init__(self.screen, (self.field_size[0], self.field_size[1] - OFFSET_Y))
        if self.is_paused:
            return
        if getInput.isKeyDown(pygame.K_LEFT, pygame.K_a):
            self.horizontal_move(-1)
        elif getInput.isKeyDown(pygame.K_RIGHT, pygame.K_d):
            self.horizontal_move(1)
        elif getInput.isKeyDown(pygame.K_UP, pygame.K_w):
            self.rotate_figure()
        elif getInput.isKeyDown(pygame.K_DOWN, pygame.K_s):
            self.move_down()
        elif getInput.isKeyDown(pygame.K_SPACE):
            self.drop_figure()

    def pause(self):
        self.is_paused = not self.is_paused

    def update(self):
        if getInput.is_move() and not self.is_paused:
            self.move_down()

        self.check_input()
        self.render()


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.buttons = pygame.sprite.Group()
        self.color = 1

        pygame.time.set_timer(pygame.USEREVENT + 1, 400)

        Button((screen_size[0] // 4, 300), (screen_size[0] // 2, 100), "Play", (0, 0, 0), COLORS[2], COLORS[4],
               70, Options.play.value, self.buttons)
        Button((screen_size[0] // 4, 430), (screen_size[0] // 2, 100), "Quit", (0, 0, 0), COLORS[2], COLORS[4],
               70, Options.quit.value, self.buttons)

    def check_input(self):
        for el in self.buttons:
            if el.rect.collidepoint(pygame.mouse.get_pos()):
                el.hover()
                if any(pygame.mouse.get_pressed()):
                    eval(f"{OPTION_LIST[el.get_option()]}()")

    def draw_logo(self):
        font = pygame.font.Font("assets/fonts/Tetris.ttf", 72)
        text = font.render("TETRIS", True, COLORS[self.color])
        self.screen.blit(text, (screen_size[0] // 2 - text.get_width() // 2, 60))

    def change_logo_color(self):
        self.color += 1
        if self.color >= len(COLORS):
            self.color = 1

    def update(self):
        self.screen.fill((0, 0, 0))
        self.buttons.update()
        self.buttons.draw(self.screen)
        self.check_input()

        if getInput.check_event(pygame.USEREVENT + 1):
            self.change_logo_color()
        self.draw_logo()