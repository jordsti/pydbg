__author__ = 'JordSti'

import gui
import os
import pygame
import cards


class deck_view(gui.gui_state):

    def __init__(self, library=None):
        gui.gui_state.__init__(self)

        if library is None:
            library = cards.library("../dc-deck/pack1")

        self.library = library
        self.handle_quit = False
        self.pic_cards = []
        self.current_index = 0
        self.key_downs = []

        self.deck_start_x = 0

        self.card_offset = 15

        self.lbl_current_card = gui.label()
        self.lbl_cards_count = gui.label()
        self.lbl_deck_name = gui.label()

        self.deck_combo = gui.combobox(120, 20)
        self.deck_combo.items.append("Pack1")
        self.deck_combo.items.append("Pack2")
        self.deck_combo.items.append("Pack3")
        self.deck_combo.items.append("Pack4")

        self.btn_back = gui.button()
        self.btn_back.width = 120
        self.btn_back.height = 35
        self.btn_back.caption = "Back"
        self.btn_back.add_receivers(self.back)
        self.tick_id = 0

    def back(self, src):
        import main_menu
        state = main_menu.main_menu()

        self.viewport.push(state)

    def on_event(self, event):
        if event.type == pygame.KEYUP:
            self.key_downs.remove(event.key)
        elif event.type == pygame.KEYDOWN:
            self.key_downs.append(event.key)
        else:
            gui.gui_state.on_event(self, event)

    def tick_keys(self):
        for k in self.key_downs:
            if k == pygame.K_RIGHT:
                self.current_index += 1
                self.replace_cards()
            elif k == pygame.K_LEFT:
                self.current_index -= 1
                self.replace_cards()

    def tick(self):

        if self.tick_id % 2 == 0:
            self.tick_keys()

        self.tick_id += 1

    def replace_cards(self):

        if self.current_index >= len(self.library.cards):
            self.current_index %= len(self.library.cards)
        elif self.current_index < 0:
            self.current_index += len(self.library.cards)

        index = 0
        current_x = 10
        y_pos = None
        for pb in self.pic_cards:

            if y_pos is None:
                y_pos = pb.y

            pb.x = current_x
            pb.y = y_pos

            current_x += self.card_offset

            if index == self.current_index:
                current_x += pb.width

            index += 1

        c = self.get_current_card()
        self.lbl_current_card.text = "Name : %s" % c.name
        try:
            self.lbl_cards_count.text = "Count : %d" % self.library.cards_count[c.name]
        except KeyError as e:
            self.lbl_cards_count.text = "Count : N/A"

    def get_current_card(self):
        return self.library.cards[self.current_index]

    def cbox(self, src, item):
        print "Selection changed for : " + item

    def init(self):

        #load card images and place them
        index = 0
        current_x = 10
        y_pos = None

        self.btn_back.x = 10
        self.btn_back.y = self.height - 10 - self.btn_back.height

        self.lbl_current_card.x = 10
        self.lbl_current_card.y = 50
        self.lbl_current_card.text = "Card : "

        self.lbl_cards_count.x = 10
        self.lbl_cards_count.y = 70
        self.lbl_cards_count.text = "Count : "

        self.lbl_deck_name.x = 10
        self.lbl_deck_name.y = 30
        self.lbl_deck_name.text = self.library.name

        self.deck_combo.x = self.width - 50 - self.deck_combo.width
        self.deck_combo.y = 15
        self.deck_combo.add_receiver(self.cbox)

        self.add(self.lbl_current_card)
        self.add(self.lbl_cards_count)
        self.add(self.lbl_deck_name)
        self.add(self.btn_back)
        self.add(self.deck_combo)

        for c in self.library.cards:
            img_path = os.path.join(self.library.lib_dir, c.image_path)

            pb = gui.picturebox(img_path)

            pb.scale(2.5)

            if y_pos is None:
                y_pos = (self.height - pb.height) / 2

            pb.x = current_x
            pb.y = y_pos

            if index == self.current_index:
                current_x += self.card_offset + pb.width
            else:
                current_x += self.card_offset

            self.pic_cards.append(pb)
            self.add(pb)

            index += 1

        c = self.get_current_card()

        self.lbl_current_card.text = "Name : %s" % c.name
        self.lbl_cards_count.text = "Count : %d" % self.library.cards_count[c.name]