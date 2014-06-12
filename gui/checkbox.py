__author__ = 'JordSti'
from widget import widget
import pygame


class checkbox(widget):
    (Normal, Checked) = ("gui/images/checkbox.png", "gui/images/checkbox_checked.png")

    def __init__(self, width=0, height=0):
        widget.__init__(self, "checkbox", width, height)
        self.normal_image = pygame.image.load(self.Normal)
        self.checked_image = pygame.image.load(self.Checked)
        self.state_changed = None
        self.checked = False

        self.width = self.normal_image.get_width()
        self.height = self.normal_image.get_height()

    def on_click(self, button, rel_x, rel_y):
        self.checked = not self.checked
        self.state_change()

    def state_change(self):
        if self.state_changed is not None:
            self.state_changed(self)

    def render(self):
        if self.checked:
            return self.checked_image
        else:
            return self.normal_image