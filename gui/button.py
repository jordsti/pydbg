__author__ = 'JordSti'

from widget import *
import pygame
import font


class button(highlight_widget):

    def __init__(self, width=0, height=0):
        highlight_widget.__init__(self, "button", width, height)
        self.caption = ""
        self.font = font.get_font()
        self.__receivers = []

    def add_receivers(self, receiver):
        self.__receivers.append(receiver)

    def on_click(self, btn, rel_x, rel_y):
        #button check todo
        for r in self.__receivers:
            r(self)

    def render(self):

        if self.hover:
            color1 = self.highlight_background_color
            color2 = self.highlight_foreground_color
        else:
            color1 = self.background_color
            color2 = self.foreground_color

        buffer = pygame.Surface((self.width, self.height))
        buffer.fill(color1)

        text = self.font.render(self.caption, True, color2)

        dst_rect = pygame.Rect((self.width - text.get_width())/2, (self.height - text.get_height())/2, text.get_width(), text.get_height())

        buffer.blit(text, dst_rect)

        dst_rect.width = self.width
        dst_rect.height = self.height
        dst_rect.x = 0
        dst_rect.y = 0
        pygame.draw.rect(buffer, color2, dst_rect, 1)

        return buffer