__author__ = 'JordSti'
import os
import ability


class superhero:

    def __init__(self, library):
        self.name = ""
        self.active = True
        self.image_path = ""
        self.library = library
        self.abilities = []

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
            elif l.startswith("ability:"):
                ab = l[8:]
                abi = ability.ability()
                abi.from_string(ab)
                self.abilities.append(abi)

    def get_image_path(self):
        return os.path.join(self.library.lib_dir, self.image_path)