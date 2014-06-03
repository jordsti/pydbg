__author__ = 'JordSti'

import gui
from game_object import game_object
import cards
import pygame


class game_state(gui.gui_state):

    def __init__(self, players):
        gui.gui_state.__init__(self)
        self.library = cards.library("deck/pack1")
        self.game = game_object(self.library)

        for p in players:
            self.game.add_player(p)

        self.handle_quit = False

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            print event.unicode