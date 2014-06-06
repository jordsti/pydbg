__author__ = 'JordSti'
import gui
import pygame


class card_selector(gui.widget):

    def __init__(self, cards, width=0, height=0):
        gui.widget.__init__(self, "card_selector", width, height)
        self.cards = cards

        self.selected_cards = []

        self.cards_image = {}

        self.card_width = 310
        self.card_height = 440

        self.card_y_offset = 10
        self.card_x_offset = 100

        self.load_images()

        self.card_position = 0

    def load_images(self):

        for card in self.cards:
            img = pygame.image.load(card.get_image_path())
            img = pygame.transform.scale(img, (self.card_width, self.card_height))

            self.cards_image[card] = img

    def on_key(self, event):

        if event.key == pygame.KEYDOWN and self.card_position > 0:
            self.card_position -= 1
        elif event.key == pygame.KEYUP and self.card_position < len(self.cards):
            self.card_position += 1


    def render(self):

        buffer = pygame.Surface((self.width, self.height))

        buffer.fill(self.background_color)

        card_pos = pygame.Rect(0, 0, self.card_width, self.card_height)
        #drawing  cards

        cur_y = self.height - self.card_y_offset
        ic = 0
        for card in self.cards:
            if card not in self.selected_cards:
                card_pos.x = 10
                card_pos.y = cur_y

                if ic == self.card_position:
                    cur_y -= self.card_height
                else:
                    cur_y -= self.card_y_offset
                ic += 1

                buffer.blit(self.cards_image[card], card_pos)
            #todo
            #else:



        border = pygame.Rect(0, 0, self.width, self.height)

        pygame.draw.rect(buffer, self.foreground_color, border, 2)

        return buffer

