__author__ = 'JordSti'

from gui import widget
import pygame

class card_widget:

    def __init__(self, card=None, width=0, height=0):
        widget.__init__("card_widget", width, height)
        self.card = card

        self.raw_image = pygame.image.load()
