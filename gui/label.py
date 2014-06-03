__author__ = 'JordSti'

from widget import widget
import pygame
import font


class label(widget):

    def __init__(self, width=0, height=0):
        widget.__init__(self, "label", width, height)
        self.font = font.get_font()
        self.text = ""
        self.auto_size = True

    def render(self):

        buffer = pygame.Surface((self.width, self.height))

        text = self.font.render(self.text, True, self.foreground_color)

        if self.width == 0 and self.height == 0:
            self.width = text.get_width()
            self.height = text.get_height()
        elif not self.width == text.get_width() or not self.height == text.get_height() and self.auto_size:
            self.width = text.get_width()
            self.height = text.get_height()

        dst_rect = pygame.Rect((self.width - text.get_width())/2, (self.height - text.get_height())/2, text.get_width(), text.get_height())

        buffer.blit(text, dst_rect)

        return buffer