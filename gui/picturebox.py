__author__ = 'JordSti'

from widget import widget
import pygame
import math

class picturebox(widget):

    def __init__(self, image_path, width=0, height=0):
        widget.__init__(self, "picturebox", width, height)
        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)

        if self.width == 0 and self.height == 0:
            self.width = self.image.get_width()
            self.height = self.image.get_height()
        elif self.width < self.image.get_width or self.height < self.image.get_height():
            self.image = pygame.transform.scale(self.image, (self.width, self.height))


    def scale(self, divisor):
        self.width = int(math.ceil(self.width / divisor))
        self.height = int(math.ceil(self.height / divisor))

        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def render(self):
        #todo
        return self.image
