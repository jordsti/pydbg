__author__ = 'JordSti'

import os
import card
import superhero


class library:

    def __init__(self, lib_dir):
        self.lib_dir = lib_dir
        self.name = ""
        self.cards_count = {}
        self.cards = []
        self.supervilains = []
        self.starter_cards = {}
        self.curse_card = None
        self.buyable_power = None
        self.superheroes = []
        self.first_supervilain = None

        fp = open(os.path.join(lib_dir, "library"), "r")

        lines = fp.readlines()

        fp.close()

        for l in lines:
            l = l.rstrip('\n').rstrip('\r')
            if not l.startswith("#"):
                if l.startswith("name:"):
                    self.name = l[5:]
                elif l.startswith("count:"):
                    l = l[6:]
                    data = l.split(",")
                    self.cards_count[data[0]] = int(data[1])
                elif l.startswith("starter:"):
                    l = l[8:]
                    data = l.split(",")
                    self.starter_cards[data[0]] = int(data[1])
                elif l.startswith("curse:"):
                    self.curse_card = l[6:]
                elif l.startswith("buyable_power:"):
                    self.buyable_power = l[14:]
                elif l.startswith("first_supervilain:"):
                    self.first_supervilain = l[18:]

        files = os.listdir(lib_dir)

        for f in files:
            path = os.path.join(lib_dir, f)
            if os.path.isfile(path) and path.endswith(".card"):
                #card to load
                c = card.card()
                c.from_file(path)
                self.cards.append(c)

            elif os.path.isfile(path) and path.endswith(".superhero"):
                s = superhero.superhero(self)
                s.from_file(path)
                self.superheroes.append(s)

            elif os.path.isfile(path) and path.endswith(".supervilain"):
                sv = card.card()
                sv.from_file(path)

                self.supervilains.append(sv)

    def get_starter(self):

        cards = []

        for k in self.starter_cards:
            nb = self.starter_cards[k]
            card = self.get_card_by_name(k)
            for i in range(nb):
                cards.append(card)

        return cards

    def get_supervilain_by_name(self, name):

        for sv in self.supervilains:
            if sv.name == name:
                return sv

        return None

    def get_superhero_by_name(self, name):

        for sh in self.superheroes:
            if sh.name == name:
                return sh

        return None

    def get_card_by_name(self, name):

        for c in self.cards:
            if c.name == name:
                return c

        return None