__author__ = 'JordSti'
import os


class card:

    def __init__(self):
        self.name = ""
        self.card_type = ""
        self.image_path = ""
        self.cost = 0
        self.value = 0
        #many things to add

    def from_file(self, filepath):

        fp = open(filepath, 'r')

        lines = fp.readlines()

        fp.close()

        for l in lines:
            l = l.rstrip('\n').rstrip('\r')
            if l.startswith("name:"):
                self.name = l[5:]
            elif l.startswith("card_type:"):
                self.card_type = l[10:]
            elif l.startswith("image_path:"):
                self.image_path = l[11:]
            elif l.startswith("cost:"):
                self.cost = int(l[5:])
            elif l.startswith("value:"):
                self.value = int(l[6:])


game_card_id = 0


def get_card_id():

    global game_card_id

    cid = game_card_id

    game_card_id += 1

    return cid


class game_card(card):

    def __init__(self, card_id, library):
        card.__init__(self)
        self.library = library
        self.card_id = get_card_id()
        self.name = card_id.name
        self.card_type = card_id.card_type
        self.image_path = card_id.image_path
        self.cost = card_id.cost
        self.value = card_id.value

    def get_image_path(self):
        p = os.path.join(self.library.lib_dir, self.image_path)
        return p