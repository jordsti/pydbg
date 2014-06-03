__author__ = 'JordSti'
import os


class superhero:

    def __init__(self, library):
        self.name = ""
        self.image_path = ""
        self.library = library
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

    def get_image_path(self):
        return os.path.join(self.library.lib_dir, self.image_path)