__author__ = 'JordSti'
import pygame


class widget:

    def __init__(self, widget_name="widget", width=0, height=0):
        self.widget_name = widget_name
        self.width = width
        self.height = height
        self.x = 0
        self.y = 0
        self.visible = True

        self.background_color = 0, 0, 0
        self.foreground_color = 250, 250, 250

        self.hover = False

    def is_hover(self, hover):
        self.hover = hover

    def render(self):
        buffer = pygame.Surface((self.width, self.height))

        buffer.fill(self.background_color)

        return buffer

    def on_click(self, button, rel_x, rel_y):
        pass

    def on_mouse_over(self, rel_x, rel_y):
        pass

    def on_key(self, event):
        pass

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def middle(self, dimension):
        self.x = (dimension.width - self.width)/2
        self.y = (dimension.height - self.height)/2

    def contains(self, x, y):
        return self.x <= x and self.y <= y and self.x + self.width >= x and self.y + self.height >= y


class highlight_widget(widget):

    def __init__(self, widget_name="widget", width=0, height=0):
        widget.__init__(self, widget_name, width, height)

        self.highlight_background_color = 150, 150, 150
        self.highlight_foreground_color = 10, 10, 10

