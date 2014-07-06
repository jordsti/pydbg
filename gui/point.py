__author__ = 'JordSti'
import math


class point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, pt):
        self.x += pt.x
        self.y += pt.y

    def subtract(self, pt):
        self.x -= pt.x
        self.y -= pt.y

    def distance(self, pt):
        return math.sqrt(math.pow(pt.x - self.x, 2) + math.pow(pt.y - self.y))
