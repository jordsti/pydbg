__author__ = 'JordSti'

import gui
from game_object import *
from card_widget import card_widget
from player_widget import player_widget
from card_selector import *
import cards
import pygame


class game_state(gui.gui_state):
    (RandomPick, ChosenPick) = (0, 1)

    def __init__(self, players, superhero_pick=RandomPick, players_pick={}):
        gui.gui_state.__init__(self)
        self.library = cards.library("../dc-deck/pack1")  # todo need to find a more elegant way, not to hardcode this!
        self.game = game_object(self.library)
        self.players_cards = []
        self.played_cards = []
        self.player_widgets = []
        self.supervilain_widget = None
        self.superhero_pick = superhero_pick
        self.players_pick = players_pick

        self.current_player = None

        self.lineup_width = 106
        self.lineup_height = 150

        self.zoom_width = 424
        self.zoom_height = 600
        self.choice_overlay = None

        for p in players:
            self.game.add_player(p)

        self.handle_quit = True

        self.card_zoomed = False
        self.zoomed_widget = None

        self.game.roll_players_start()

        if self.superhero_pick == self.RandomPick:
            self.game.pick_superhero()
        elif self.superhero_pick == self.ChosenPick:
            self.game.assign_superhero(players_pick)

        self.game.create_cards()

        self.supervilain_widget = card_widget(self, self.game.current_supervilain, 106, 150)
        self.supervilain_widget.zoom_width = 424
        self.supervilain_widget.zoom_height = 600
        self.add(self.supervilain_widget)

        current_y = 0

        for p in self.game.players:
            widget = player_widget(p, 300, 120)
            widget.y = current_y
            self.add(widget)
            self.player_widgets.append(widget)
            current_y += widget.height

        self.lineups = []

        self.lineups_empty_case = []

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

        self.supervilain_widget.x = l_start_x - 121
        self.supervilain_widget.y = l_start_y + self.buyable_power_stack.height + 10

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
        self.lbl_current_turn.text = "%s turns" % self.game.get_current_player().name

        self.lbl_current_turn.x = 5
        self.lbl_current_turn.y = 5

        self.add(self.lbl_current_turn)

        self.lbl_hand = gui.label()
        self.lbl_hand.text = "Hand :"
        self.lbl_hand.x = 10
        self.lbl_hand.y = 160

        self.add(self.lbl_hand)


        self.hand_x = 70
        self.hand_y = 160
        self.hand_width = 91
        self.hand_height = 130

        self.play_x = 70
        self.play_y = 20
        self.play_width = 91
        self.play_height = 130

        #todo need a place for gained cards, or a widget that pop up on button..
        self.gained_card_x = 0
        self.gained_card_y = 0

        #quit to main menu button
        self.btn_quit_game = gui.button(200, 30)
        self.btn_quit_game.x = 10
        self.btn_quit_game.y = 10
        self.btn_quit_game.caption = "Quit game"
        self.btn_quit_game.add_receivers(self.quit_game)

        self.btn_end_turn = gui.button(200, 50)
        self.btn_end_turn.caption = "End turn"
        self.btn_end_turn.add_receivers(self.end_turn)

        self.game.change_turn = self.player_turn
        self.game.card_played = self.played_card
        self.game.lineup_changed = self.apply_lineup_action
        self.buyable_power_stack.activated = self.buy_card
        self.game.drawn_card = self.drawn_card
        self.game.ask_player = self.ask_player
        self.game.start_game()

    def ask_player(self, player, choice):
        if self.choice_overlay is None:
            selector = card_selector(choice.cards, choice, self.width - 300, self.height - 100)
            selector.middle(self)
            selector.closing = self.close_overlay
            self.choice_overlay = selector
        else:
            #pending support todo
            pass

    def drawn_card(self, player, card):
        #take empty hand card place todo
        cx = 0

        for w in self.players_cards:
            if w.x > cx:
                cx = w.x

        cx += 10
        cx += self.play_width

        w = card_widget(self, card, self.hand_width, self.hand_height)
        w.zoom_width = self.zoom_width
        w.zoom_height = self.zoom_height
        w.activated = self.play_card

        w.x = cx
        w.y = self.hand_y

        self.add(w)
        self.players_cards.append(w)


    def buy_card(self, widget, card):
        if card in self.game.buyable_powers:
            rs = self.game.buy_card(card)

            if rs and len(self.game.buyable_powers) > 0:
                self.buyable_power_stack.card = self.game.buyable_powers[0]
            elif len(self.game.buyable_powers) == 0:
                self.elements.remove(self.buyable_power_stack)

        else:
            self.game.buy_card(card)

    def played_card(self, player, card):
        widget = card_widget(self, card, self.play_width, self.play_height)
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
        widget.zoom_width = self.zoom_width
        widget.zoom_height = self.zoom_height

        self.played_cards.append(widget)
        self.add(widget)

        for c_widget in self.players_cards:
            if c_widget.card == card:
                self.elements.remove(c_widget)
                self.players_cards.remove(c_widget)
                break

    def end_turn(self, src):
        #removing played cards

        for c in self.played_cards:
            self.elements.remove(c)

        self.played_cards = []

        self.game.end_turn_phase()
        self.elements.remove(self.btn_end_turn)

    def close_overlay(self, src):
        #completing choice
        #need to check if the choice is may or forced and respecting card count
        #todo
        selected_cards = self.choice_overlay.selected_cards
        self.game.complete_choice(self.choice_overlay.choice)

        self.choice_overlay = None

    def quit_game(self, src):
        import main_menu
        state = main_menu.main_menu()
        self.viewport.push(state)

    def apply_lineup_action(self, actions):
        for a in actions:
            if a.type == lineup_action.Removed:
                for w in self.lineups:
                    if a.card == w.card:
                        self.lineups.remove(w)
                        self.elements.remove(w)
                        pt = gui.point(w.x, w.y)
                        self.lineups_empty_case.append(pt)
            elif a.type == lineup_action.Added:
                pt = self.lineups_empty_case[0]
                self.lineups_empty_case.remove(pt)

                w = card_widget(self, a.card, self.lineup_width, self.lineup_height)
                w.x = pt.x
                w.y = pt.y
                w.zoom_width = self.zoom_width
                w.zoom_height = self.zoom_height

                self.add(w)
                self.lineups.append(w)

    def refresh_lineups(self):

        for w in self.lineups:
            w.activated = self.buy_card

        if len(self.game.buyable_powers) > 0:
            self.buyable_power_stack.activated = self.buy_card

    def player_turn(self, player):
        print "turn-> " + player.name
        self.lbl_current_turn.text = "%s's turn !" % player.name
        self.current_player = player
        #card view
        cards = player.hand

        ix = 0
        for c in cards:
            widget = card_widget(self, c, self.hand_width, self.hand_height)
            widget.x = self.hand_x + ix
            widget.y = self.hand_y
            widget.zoom_width = self.zoom_width
            widget.zoom_height = self.zoom_height
            self.players_cards.append(widget)
            self.add(widget)
            widget.activated = self.play_card
            ix += widget.width + 10

        self.refresh_lineups()


    def play_card(self, widget, card):
        self.game.play_card(self.current_player, card)

    def tick(self):
        if self.current_player is not None:
            if len(self.current_player.hand) == 0:
                if self.btn_end_turn not in self.elements:
                    self.btn_end_turn.x = self.hand_x
                    self.btn_end_turn.y = self.hand_y
                    self.add(self.btn_end_turn)

    def init(self):
        for w in self.player_widgets:
            w.x = self.width - w.width

    def on_event(self, event):
        if self.choice_overlay is not None:
            if event.type == pygame.KEYUP or event.type == pygame.KEYDOWN:
                self.choice_overlay.on_key(event)
            elif event.type == pygame.MOUSEMOTION:
                r_x = event.pos[0] - self.choice_overlay.x
                r_y = event.pos[1] - self.choice_overlay.y
                if self.choice_overlay.contains(r_x, r_y):
                    self.choice_overlay.on_mouse_over(r_x, r_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                r_x = event.pos[0] - self.choice_overlay.x
                r_y = event.pos[1] - self.choice_overlay.y
                if self.choice_overlay.contains(r_x, r_y):
                    self.choice_overlay.on_click(event.button, r_x, r_y)
        else:
            gui.gui_state.on_event(self, event)

        if event.type == pygame.QUIT:
            import main_menu
            state = main_menu.main_menu()
            self.viewport.push(state)

    def paint(self, screen):

        gui.gui_state.paint(self, screen)

        if self.choice_overlay is not None:
            rect = pygame.Rect(self.choice_overlay.x, self.choice_overlay.y, self.choice_overlay.width, self.choice_overlay.height)

            screen.blit(self.choice_overlay.render(), rect)
