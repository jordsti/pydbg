__author__ = 'JordSti'

from gui import widget
import pygame


class card_widget(widget):

    def __init__(self, state, card=None, width=0, height=0):
        widget.__init__(self, "card_widget", width, height)

        self.btn_width = 120
        self.btn_height = 30

        self.activated = None

        self.card = card
        self.state = state
        if card is not None:
            self.raw_image = pygame.image.load(self.card.get_image_path())
        self.image = None
        self.can_zoom = True
        self.zoomed = False

        self.zoom_width = self.raw_image.get_width()
        self.zoom_height = self.raw_image.get_height()

        self.last_x = 0
        self.last_y = 0
        self.last_width = 0
        self.last_height = 0

        if self.width < self.raw_image.get_width() or self.height < self.raw_image.get_height():
            #resize
            self.resize(self.width, self.height)
        else:
            self.image = self.raw_image

    def on_click(self, button, rel_x, rel_y):
        if not self.zoomed and self.can_zoom and not self.state.card_zoomed:
            #zoom to 100%
            width = self.zoom_width
            height = self.zoom_height
            self.last_x = self.x
            self.last_y = self.y
            self.last_width = self.width
            self.last_height = self.height

            self.x = (self.state.width - width) / 2
            self.y = (self.state.height - height) / 2
            self.width = width
            self.height = height

            self.state.bring_to_top(self)
            self.zoomed = True

            self.resize(width, height)

            self.state.card_zoomed = True

            self.state.zoomed_widget = self

        elif self.zoomed:
            self.state.card_zoomed = False
            self.x = self.last_x
            self.y = self.last_y
            self.resize(self.last_width, self.last_height)
            self.zoomed = False

    def resize(self, width, height):
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(self.raw_image, (self.width, self.height))

    def on_key(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if self.zoomed and self.state.zoomed_widget == self:
                    self.zoomed = False
                    self.x = self.last_x
                    self.y = self.last_y
                    self.resize(self.last_width, self.last_height)
                    self.state.card_zoomed = False
            elif event.key == pygame.K_RETURN:
                if self.zoomed and self.state.zoomed_widget == self:
                    self.zoomed = False
                    self.x = self.last_x
                    self.y = self.last_y
                    self.resize(self.last_width, self.last_height)
                    self.state.card_zoomed = False
                    if self.activated is not None:
                        self.activated(self, self.card)

    def render(self):
        return self.image