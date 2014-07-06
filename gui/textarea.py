__author__ = 'JordSti'
from widget import widget
import font
import pygame


class textarea(widget):
    (LineSeparator, LineOffset) = ('\n', 2)

    def __init__(self, width=0, height=0):
        widget.__init__(self, "textarea", width, height)

        self.font = font.get_font()
        self.line_height = self.font.size('a')[1]
        self.line_offset = self.LineOffset
        self.line_separator = self.LineSeparator

        self.text = ""

    def append(self, new_line):
        self.text += self.line_separator + new_line

    def render(self):
        buffer = pygame.Surface((self.width, self.height))

        buffer.fill(self.background_color)

        rect = self.get_rect()
        rect.x = 0
        rect.y = 0
        #border
        pygame.draw.rect(buffer, self.foreground_color, rect, 1)

        lines = self.text.split(self.line_separator)

        #start at end

        current_y = self.height - self.line_height - self.line_offset

        nb_lines = len(lines)
        i = nb_lines-1
        while current_y > 0 and i >= 0:
            line = lines[i]
            text = self.font.render(line, True, self.foreground_color)
            rect.x = 2
            rect.y = current_y
            rect.w = text.get_width()
            rect.h = text.get_height()
            buffer.blit(text, rect)
            current_y -= self.line_height - self.line_offset
            i -= 1

        return buffer