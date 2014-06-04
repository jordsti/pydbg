__author__ = 'JordSti'

import gui
from game_object import game_object
from card_widget import card_widget
from player_widget import player_widget
import cards
import pygame


class game_state(gui.gui_state):

    def __init__(self, players):
        gui.gui_state.__init__(self)
        self.library = cards.library("deck/pack1")
        self.game = game_object(self.library)
        self.players_cards = []
        self.played_cards = []
        self.player_widgets = []

        for p in players:
            self.game.add_player(p)

        self.handle_quit = False

        self.card_zoomed = False

        self.game.pick_superhero()

        self.game.create_cards()

        current_y = 0

        for p in self.game.players:
            widget = player_widget(p, 300, 120)
            widget.y = current_y
            self.add(widget)
            self.player_widgets.append(widget)
            current_y += widget.height


        self.lineups = []

        self.curse_stack = card_widget(self, self.game.curses[0], 106, 150)

        self.buyable_power_stack = card_widget(self, self.game.buyable_powers[0], 106, 150)

        self.add(self.curse_stack)
        self.add(self.buyable_power_stack)

        l_start_x = 250
        l_start_y = 300


        self.curse_stack.x = l_start_x - 121*2
        self.curse_stack.y = l_start_y
        self.curse_stack.zoom_width = 424
        self.curse_stack.zoom_height = 600

        self.buyable_power_stack.x = l_start_x - 121
        self.buyable_power_stack.y = l_start_y
        self.buyable_power_stack.zoom_width = 424
        self.buyable_power_stack.zoom_height = 600

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

        #turn info
        self.lbl_current_turn = gui.label()
        self.lbl_current_turn.text = "%s turns" % (self.game.get_current_player().name)

        self.lbl_current_turn.x = 10
        self.lbl_current_turn.y = 100

        self.add(self.lbl_current_turn)

        self.lbl_hand = gui.label()
        self.lbl_hand.text = "Hand :"
        self.lbl_hand.x = 10
        self.lbl_hand.y = 160

        self.add(self.lbl_hand)

        self.hand_x = 70
        self.hand_y = 160

        self.play_x = 70
        self.play_y = 20

        #quit to main menu button
        self.btn_quit_game = gui.button(200, 30)
        self.btn_quit_game.x = 10
        self.btn_quit_game.y = 10
        self.btn_quit_game.caption = "Quit game"
        self.btn_quit_game.add_receivers(self.quit_game)

        self.game.change_turn = self.player_turn
        self.game.card_played = self.played_card
        self.game.start_game()

    def played_card(self, player, card):
        widget = card_widget(self, card, 91, 130)
        if len(self.played_cards) > 0:
            last = self.played_cards[len(self.played_cards)-1]
            x = last.x + 10 + last.width
            y = self.play_y
            widget.x = x
            widget.y = y
        else:
            x = self.play_x
            y = self.play_y
            widget.x = x
            widget.y = y
        widget.zoom_width = 424
        widget.zoom_height = 600

        self.played_cards.append(widget)
        self.add(widget)

        for c_widget in self.players_cards:
            if c_widget.card == card:
                self.elements.remove(c_widget)
                self.players_cards.remove(c_widget)
                break


    def quit_game(self, src):
        import main_menu
        state = main_menu.main_menu()
        self.viewport.push(state)

    def player_turn(self, player):
        self.lbl_current_turn.text = "%s's turn !" % (player.name)
        #card view
        cards = player.hand

        ix = 0
        for c in cards:
            widget = card_widget(self, c, 91, 130)
            #maybe special widget to play a card
            widget.player = player
            widget.x = self.hand_x + ix
            widget.y = self.hand_y
            widget.zoom_width = 424
            widget.zoom_height = 600
            self.players_cards.append(widget)
            self.add(widget)
            widget.play_card = self.game.play_card
            ix += widget.width + 10

    def tick(self):
        pass

    def init(self):
        for w in self.player_widgets:
            w.x = self.width - w.width



    def on_event(self, event):
        gui.gui_state.on_event(self, event)

        if event.type == pygame.KEYDOWN:
            print event.unicode