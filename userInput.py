import pygame


class UserInput:
    def __init__(self):
        self.holding = []
        self.keys_down = []
        self.keys_up = []
        self.terminate = False
        self.is_move_frame = False
        self.events = []

    def update(self):
        self.keys_up = []
        self.keys_down = []
        self.is_move_frame = False
        self.events = pygame.event.get()
        for event in self.events:
            if event.type == pygame.QUIT:
                self.terminate = True
            elif event.type == pygame.KEYDOWN:
                self.keys_down.append(event.key)
                if event.key not in self.holding:
                    self.holding.append(event.key)
            elif event.type == pygame.KEYUP:
                self.keys_up.append(event.key)
                if event.key in self.holding:
                    self.holding.remove(event.key)
            elif event.type == pygame.USEREVENT:
                self.is_move_frame = True

    def isKeyHolding(self, *keys):
        return any([key in self.holding for key in keys])

    def isKeyDown(self, *keys):
        return any([key in self.keys_down for key in keys])

    def isKeyUp(self, *keys):
        return any([key in self.keys_up for key in keys])

    def is_move(self):
        return self.is_move_frame

    def is_terminated(self):
        return self.terminate

    def get_events(self):
        return self.events

    def check_event(self, event):
        return any([e.type == event for e in self.get_events()])