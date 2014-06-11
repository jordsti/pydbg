__author__ = 'JordSti'

import pygame


class viewport:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.background = 0, 0, 0

        self.current_state = None
        self._run = False
        self.screen = None

        self.screen = pygame.display.set_mode((width, height))

    def run(self):

        self._run = True

        while self._run:
            if self.current_state is not None:

                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        if self.current_state.handle_quit:
                            self.current_state.on_event(e)
                            continue
                        else:
                            import sys
                            sys.exit()

                    self.current_state.on_event(e)

                self.screen.fill(self.background)

                self.current_state.tick()
                self.current_state.paint(self.screen)

                pygame.display.flip()
            else:
                raise Exception("No state specified")

    def push(self, state):

        if self.current_state is not None:
            self.current_state.stop()

        self.current_state = state
        state.viewport = self
        self.current_state.width = self.width
        self.current_state.height = self.height
        self.current_state.init()

        if not self._run:
            self.run()




def create_viewport(width, height):

    pygame.init()

    v = viewport(width, height)

    return v