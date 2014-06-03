__author__ = 'JordSti'
from widget import widget
import font


class textbox(widget):

    def __init__(self, width=0, height=0):
        widget.__init__("textbox", width, height)

        self.font = font.get_font()
