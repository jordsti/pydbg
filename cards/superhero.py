__author__ = 'JordSti'


class superhero:

    def __init__(self):
        self.name = ""
        self.image_path = ""
        #abilities todo

    def from_file(self, filepath):

        fp = open(filepath, 'r')

        lines = fp.readlines()

        fp.close()

        for l in lines:
            l = l.rstrip('\n').rstrip('\r')

            if l.startswith("name:"):
                self.name = l[5:]
            elif l.startswith("image_path:"):
                self.image_path = l[11:]