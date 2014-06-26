__author__ = 'JordSti'


class style:

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

    def to_file(self, destination):
        fp = open(destination, 'w')
        fp.write(self.to_string())
        fp.close()


def load_style(style_path):
    fp = open(style_path, 'r')
    lines = fp.readlines()
    fp.close()

    loaded_style = style()

    for l in lines:
        data = l.split(':')
        rgb = data[1].replace('[', '')
        rgb = rgb.replace(']', '')
        rgb = rgb.split(',')
        
        color = int(rgb[0]), int(rgb[1]), int(rgb[2])
        if data[0] == 'foreground':
            loaded_style.foreground_color = color
        elif data[1] == 'background':
            loaded_style.background_color = color
        elif data[1] == 'highlight_foreground':
            loaded_style.highlight_foreground_color = color
        elif data[1] == 'highlight_background':
            loaded_style.highlight_background_color = color

    return loaded_style

current_style = None


def get_style():

    global current_style

    if current_style is None:
        current_style = style()

    return current_style


def set_style(style):
    global current_style
    current_style = style