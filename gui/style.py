__author__ = 'JordSti'


class style:
    #todo
    #style serialization to be added

    def __init__(self, name="default"):
        self.name = name

        self.foreground_color = 250, 250, 250
        self.background_color = 0, 0, 0

        self.highlight_foreground_color = 10, 10, 10
        self.highlight_background_color = 150, 150, 150


    def to_string(self):

        text = ""

        text += "foreground:[%d,%d,%d]\n" % (self.foreground_color[0], self.foreground_color[1], self.foreground_color[2])
        text += "background:[%d,%d,%d]\n" % (self.background_color[0], self.background_color[1], self.background_color[2])

        text += "highlight_foreground:[%d,%d,%d]\n" % (self.highlight_foreground_color[0], self.highlight_foreground_color[1], self.highlight_foreground_color[2])
        text += "highlight_background:[%d,%d,%d]\n" % (self.highlight_background_color[0], self.highlight_background_color[1], self.highlight_background_color[2])

        return text

current_style = None


def get_style():

    global current_style

    if current_style is None:
        current_style = style()

    return current_style


def set_style(style):
    global current_style
    current_style = style