__author__ = 'JordSti'
import gui
import pygame
from player import player_choice

# todo
# add reset button, to replace cards into possible choice


class card_selector(gui.widget):

    def __init__(self, cards, choice, width=0, height=0):
        gui.widget.__init__(self, "card_selector", width, height)

        self.font = gui.get_big_font()

        card_result = ""

        if choice.destination == player_choice.DiscardCard:
            card_result = "discard"
        elif choice.destination == player_choice.DestroyCard:
            card_result = "destroy"
        elif choice.destination == player_choice.PlayerDeckBottom:
            card_result = "deck bottom"
        elif choice.destination == player_choice.PlayerDeckTop:
            card_result = "deck top"

        if not choice.count == -1:
            self.title = "Choose %d card(s) to %s" % (choice.count, card_result)
        else:
            self.title = "Choose cards to %s" % card_result

        self.cards = cards

        self.possible_choice = self.cards

        self.choice = choice

        self.selected_cards = []

        self.cards_image = {}

        self.card_width = 310
        self.card_height = 440

        self.card_y_offset = 10
        self.card_x_offset = 100

        self.load_images()

        self.card_position = 0

        self.closing = None

        self.btn_accept = gui.button(100, 30)
        self.btn_accept.caption = "Accept"
        self.btn_accept.add_receivers(self.accept)

        self.btn_reset = gui.button(100, 30)
        self.btn_reset.caption = "Reset"
        self.btn_reset.add_receivers(self.reset)

        self.choice_done = None

    def reset(self, src):
        s_cards = self.selected_cards
        self.selected_cards = []

        for c in s_cards:
            self.possible_choice.append(c)

    def apply_choice(self):
        for c in self.selected_cards:
            self.choice.selected_cards.append(c)

    def accept(self, src):
        if not self.choice.may:
            if len(self.selected_cards) == self.choice.count:
                self.apply_choice()
                if self.choice_done is not None:
                    self.choice_done(self.choice)  # todo some testing
            else:
                print "You must choose %d cards !" % self.choice.count
        else:
            if self.choice_done is not None:
                self.apply_choice()
                self.choice_done(self.choice)  # todo some testing

    def load_images(self):

        for card in self.cards:
            img = pygame.image.load(card.get_image_path())
            img = pygame.transform.scale(img, (self.card_width, self.card_height))

            self.cards_image[card] = img

    def on_key(self, event):

        if event.key == pygame.K_UP and self.card_position > 0:
            self.card_position -= 1

        elif event.key == pygame.K_DOWN and self.card_position < len(self.cards):
            self.card_position += 1

        elif event.key == pygame.K_ESCAPE:
            if self.closing is not None:
                self.closing(self)

        elif event.key == pygame.K_RETURN and event.type == pygame.KEYUP:
            if len(self.possible_choice) > self.card_position:
                if len(self.selected_cards) < self.choice.count or self.choice.count == -1:
                    print "selecting card : ", self.card_position
                    card = self.possible_choice[self.card_position]
                    self.selected_cards.append(card)
                    self.possible_choice.remove(card)

                    if self.card_position == len(self.possible_choice) and self.card_position > 0:
                        self.card_position -= 1

        print "Current Card : ", self.card_position  # debug purpose

    def on_mouse_over(self, rel_x, rel_y):
        if self.btn_accept.contains(rel_x, rel_y):
            self.btn_accept.is_hover(True)
        else:
            self.btn_accept.is_hover(False)

    def on_click(self, button, rel_x, rel_y):
        if self.btn_accept.contains(rel_x, rel_y):
            self.btn_accept.on_click(button, rel_x - self.btn_accept.x, rel_y - self.btn_accept.y)
        elif self.btn_reset.contains(rel_x, rel_y):
            self.btn_reset.on_click(button, rel_x - self.btn_reset.x, rel_y - self.btn_reset.y)

    def render(self):
        buffer = pygame.Surface((self.width, self.height))
        buffer.fill(self.background_color)

        #text caption
        #top middle

        text = self.font.render(self.title, True, self.foreground_color)

        text_pos = pygame.Rect((self.width - text.get_width())/2, 10, text.get_width(), text.get_height())

        buffer.blit(text, text_pos)

        card_pos = pygame.Rect(0, 0, self.card_width, self.card_height)
        #drawing  cards

        cur_y = self.height - self.card_y_offset - self.card_height
        #cards that can be selected
        ic = 0

        for card in self.possible_choice:
            card_pos.x = 10
            card_pos.y = cur_y

            if ic == self.card_position:
                cur_y -= self.card_height
            else:
                cur_y -= self.card_y_offset
            ic += 1

            buffer.blit(self.cards_image[card], card_pos)

        #selected cards
        cur_y = self.height - self.card_y_offset - self.card_height
        for card in self.selected_cards:
            card_pos.x = self.card_x_offset + self.card_width
            card_pos.y = cur_y

            cur_y += self.card_y_offset

            buffer.blit(self.cards_image[card], card_pos)

        border = pygame.Rect(0, 0, self.width, self.height)

        pygame.draw.rect(buffer, self.foreground_color, border, 2)

        #placing reset button
        if self.btn_reset.x == 0 and self.btn_reset.y == 0:
            self.btn_reset.x = self.width - 10 - self.btn_reset.width
            self.btn_reset.y = self.height - 10 - self.btn_reset.height

        #placing accept button
        if self.btn_accept.x == 0 and self.btn_accept.y == 0:
            self.btn_accept.x = self.width - 10 - self.btn_accept.width
            self.btn_accept.y = self.btn_reset.y - 10 - self.btn_accept.height

        buffer.blit(self.btn_accept.render(), self.btn_accept.get_rect())
        buffer.blit(self.btn_reset.render(), self.btn_reset.get_rect())

        return buffer

