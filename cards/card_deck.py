__author__ = 'JordSti'
import random


class card_deck:

    def __init__(self):
        self.__cards = []

    def push(self, card):
        self.__cards.append(card)

    def count(self):
        return len(self.__cards)

    def pop(self):
        i = len(self.__cards)
        if i > 0:
            i -= 1
            c = self.__cards[i]
            self.__cards.remove(c)
            return c
        else:
            raise Exception("No more card!")

    def reveal(self):
        c = self.__cards[-1]
        #debug trace
        print "Revealed : %s" % c.name
        return c

    def empty(self):
        return len(self.__cards) == 0

    def shuffle(self, nb=100):

        for i in range(nb):
            i1 = random.randint(0, len(self.__cards) - 1)
            i2 = random.randint(0, len(self.__cards) - 1)

            card1 = self.__cards[i1]
            card2 = self.__cards[i2]

            self.__cards[i1] = card2
            self.__cards[i2] = card1