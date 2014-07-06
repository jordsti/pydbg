__author__ = 'JordSti'

import widget
import pygame
import font


class slider(widget.widget):

    (LeftArrow, RightArrow) = ('gui/images/arrow_left.png', 'gui/images/arrow_right.png')

    def __init__(self, width=0, height=0):
        widget.widget.__init__(self, "slider", width, height)

        self.items = []
        self.selected_index = 0

        self.font = font.get_font()

        self.left_arrow = pygame.image.load(self.LeftArrow)
        self.right_arrow = pygame.image.load(self.RightArrow)

        self.selection_changed = None

        if width == 0 and height == 0:
            self.width = self.left_arrow.get_width() + self.right_arrow.get_width() + 50
            self.height = self.left_arrow.get_height()

    def on_click(self, button, rel_x, rel_y):
        #left arrow test
        #just testing x is ok
        #wrap around if last or first item
        if rel_x < self.left_arrow.get_width():

            if self.selected_index > 0:
                self.selected_index -= 1
            else:
                self.selected_index = len(self.items) - 1

            self.__selection_changed()

        #right arrow test
        elif rel_x > self.width - self.right_arrow.get_width():

            if self.selected_index < len(self.items) - 1:
                self.selected_index += 1
            else:
                self.selected_index = 0

            self.__selection_changed()

    def __selection_changed(self):
        if self.selection_changed is not None:
            self.selection_changed(self, self.get_current_item())

    def get_item(self):
        if self.selected_index < len(self.items):
            return self.items[self.selected_index]
        else:
            return None

    def get_current_item(self):
        print "WHERE'S THIS CALL!!?!"
        return self.get_item()

    def render(self):
        buffer = pygame.Surface((self.width, self.height))

        buffer.fill(self.background_color)

        rect = pygame.Rect(0, 0, 0, 0)

        #current item
        if self.selected_index < len(self.items):
            caption = self.font.render(self.items[self.selected_index], True, self.foreground_color, self.background_color)

            rect.x = self.left_arrow.get_width() + 3
            rect.y = (self.height - caption.get_height()) / 2
            rect.w = caption.get_width()
            rect.h = caption.get_height()

            buffer.blit(caption, rect)

        #left arrow
        rect.x = 0
        rect.y = 0
        rect.w = self.left_arrow.get_width()
        rect.h = self.left_arrow.get_height()

        buffer.blit(self.left_arrow, rect)

        #right arrow
        rect.x = self.width - self.right_arrow.get_width()
        rect.y = 0
        rect.w = self.right_arrow.get_width()
        rect.h = self.left_arrow.get_height()

        buffer.blit(self.right_arrow, rect)

        #border drawing
        rect.x = 0
        rect.y = 0
        rect.width = self.width
        rect.height = self.height

        pygame.draw.rect(buffer, self.foreground_color, rect, 1)

        return buffer