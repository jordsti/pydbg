__author__ = 'JordSti'
from widget import widget
import font
import pygame


class textbox(widget):

    def __init__(self, width=0, height=0):
        widget.__init__(self, "textbox", width, height)
        self.font = font.get_font()
        self.text = ""
        self.tick = 0
        self.text_changed = None

    def on_click(self, button, rel_x, rel_y):
        if not self.focus:
            self.focus = True
        else:
            self.focus = False

    def on_key(self, event):
        if self.focus:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[0:-1]
                    self.text_change()
                elif event.key == pygame.K_RETURN:
                    self.focus = False
                else:
                    text = event.unicode
                    self.text += text
                    self.text_change()

    def text_change(self):
        if self.text_changed is not None:
            self.text_changed(self)

    def render(self):

        buffer = pygame.Surface((self.width, self.height))
        buffer.fill(self.background_color)

        box_rect = pygame.Rect(0, 0, self.width, self.height)

        caption = self.text

        if self.focus:
            self.tick += 1
            if self.tick % 3 == 0:
                caption += '_'

        text = self.font.render(caption, True, self.foreground_color)

        dst_rect = pygame.Rect(2, (self.height - text.get_height()) / 2, text.get_width(), text.get_height())

        buffer.blit(text, dst_rect)

        pygame.draw.rect(buffer, self.foreground_color, box_rect, 1)

        return buffer
