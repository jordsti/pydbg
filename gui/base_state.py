__author__ = 'JordSti'

import pygame


class base_state:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.viewport = None
        self.handle_quit = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            import sys
            sys.exit()

    def paint(self, screen):
        pass

    def tick(self):
        pass

    def init(self):
        pass

    def stop(self):
        pass

