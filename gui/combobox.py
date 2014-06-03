__author__ = 'JordSti'

from widget import highlight_widget
import pygame
import font


class combobox(highlight_widget):

    def __init__(self, width=0, height=0):
        highlight_widget.__init__(self, "combobox", width, height)
        self.items = []
        self.selected_index = 0
        self.dropdown_height = 80
        self.dropdown_open = False
        self.font = font.get_font()
        self.item_height = 20

        self.__receivers = []

        if self.height == 0:
            self.height = 22

    def add_receiver(self, receiver):
        self.__receivers.append(receiver)

    def is_hover(self, hover):
        highlight_widget.is_hover(self, hover)
        if not hover and self.dropdown_open:
            self.height -= self.dropdown_height
            self.dropdown_open = False

    def on_click(self, button, rel_x, rel_y):
        if self.dropdown_open:
            if rel_y > self.height - self.dropdown_height:
                index = (rel_y - (self.height - self.dropdown_height)) / self.item_height

                if index < len(self.items):
                    self.selected_index = index
                    #selection changed
                    for r in self.__receivers:
                        r(self, self.items[index])

            self.dropdown_open = False
            self.height -= self.dropdown_height
        else:
            self.dropdown_open = True
            self.height += self.dropdown_height

    def render(self):

        color1 = self.background_color
        color2 = self.foreground_color

        if self.hover:
            color1 = self.highlight_background_color
            color2 = self.highlight_foreground_color

        buffer = pygame.Surface((self.width, self.height))

        buffer.fill(color1)

        height = self.height

        if self.dropdown_open:
            height -= self.dropdown_height

        if len(self.items) > 0:
            if self.selected_index >= len(self.items):
                self.selected_index = len(self.items) - 1

            selected = self.items[self.selected_index]

            caption = self.font.render(selected, True, color2)

            dst_rect = pygame.Rect(2, (height - caption.get_height())/2, caption.get_width(), caption.get_height())

            buffer.blit(caption, dst_rect)

        dst_rect = pygame.Rect(0, 0, self.width, self.height)
        pygame.draw.rect(buffer, color2, dst_rect, 1)

        if self.dropdown_open:
            #drawing drop
            index = 0
            drop_rect = pygame.Rect(0, height, self.width, self.dropdown_height)

            buffer.fill(self.background_color, drop_rect)
            current_y = height
            for i in self.items:
                if index <= (self.dropdown_height / self.item_height):
                    font_color = self.foreground_color
                    if index == self.selected_index:
                        bg_rect = pygame.Rect(0, current_y, self.width, self.item_height)
                        buffer.fill(self.highlight_background_color, bg_rect)
                        font_color = self.highlight_foreground_color
                    #caption
                    text = self.font.render(i, True, font_color)
                    t_x = 2
                    t_y = (self.item_height - text.get_height()) / 2

                    dst_rect = pygame.Rect(t_x, t_y + current_y, text.get_width(), text.get_height())

                    buffer.blit(text, dst_rect)

                    current_y += self.item_height

                index += 1

            #dropdown border

            pygame.draw.rect(buffer, self.foreground_color, drop_rect, 1)

        return buffer

