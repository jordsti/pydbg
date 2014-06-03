__author__ = 'JordSti'

import gui
from game_object import game_object
from card_widget import card_widget
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

        self.card_zoomed = False

        self.game.pick_superhero()

        self.game.create_cards()

        self.lineups = []

        l_start_x = 250
        l_start_y = 180

        row = 0

        for i in range(len(self.game.lineups)):
            iw = i
            if row == 1:
                iw -= 3

            widget = card_widget(self, self.game.lineups[i], 106, 150)
            self.lineups.append(widget)
            widget.x = l_start_x + 121*iw
            widget.y = l_start_y + row*160
            widget.zoom_width = 424
            widget.zoom_height = 600

            if i == 2:
                row += 1

            self.add(widget)

    def on_event(self, event):
        gui.gui_state.on_event(self, event)

        if event.type == pygame.KEYDOWN:
            print event.unicode