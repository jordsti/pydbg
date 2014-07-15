__author__ = 'JordSti'
from card_constraint import card_constraint


class card_action:
    (ChooseCard, MayDestroyCard) = (0, 1)
    (GainedCard, LineUp, MainDeckTop, PlayerDeckTop, DiscardPile, DestroyedCard, Hand, HandAndDiscardPile, BuyablePower) = (0, 1, 2, 3, 4, 5, 6, 7, 8)
    (Infinite) = -1

    def __init__(self, type=ChooseCard, source=PlayerDeckTop, destination=DiscardPile, count=Infinite, forced=False):
        self.count = count
        self.forced = forced
        self.constraints = []
        self.type = type
        self.source = source
        self.destination = destination
        self.constraints = []

    def from_string(self, text):

        _vars = text.split(':')
        nb_vars = len(_vars)

        if nb_vars >= 1:
            if _vars[0] == 'ChooseCard':
                self.type = self.ChooseCard
            elif _vars[0] == 'MayDestroyCard':
                self.type = self.MayDestroyCard

        if nb_vars >= 2:
            self.source = self.parse_loc(_vars[1])

        if nb_vars >= 3:
            self.destination = self.parse_loc(_vars[2])

        if nb_vars >= 4:
            if _vars[3] == 'Infinite':
                self.count = self.Infinite
            else:
                self.count = int(_vars[3])

        if nb_vars >= 5:
            if _vars[4] == 'True':
                self.forced = True
            else:
                self.forced = False

        if nb_vars >= 6:
            #contraints support
            const = _vars[5]

            _constraints = const.split(';')

            i = 0
            for c in _constraints:
                if len(c) > 0:
                    cc = card_constraint()
                    cc.from_string(c)
                    self.constraints.append(cc)
                    i += 1

    def respect_constraint(self, card):
        for c in self.constraints:
            if not c.pass_condition(card):
                return False

        return True

    def parse_loc(self, loc):
        if loc == 'GainedCard':
            return self.GainedCard
        elif loc == 'LineUp':
            return self.LineUp
        elif loc == 'MainDeckTop':
            return self.MainDeckTop
        elif loc == 'PlayerDeckTop':
            return self.PlayerDeckTop
        elif loc == 'DiscardPile':
            return self.DiscardPile
        elif loc == 'DestroyedCard':
            return self.DestroyedCard
        elif loc == 'Hand':
            return self.Hand
        elif loc == 'HandAndDiscardPile':
            return self.HandAndDiscardPile
        elif loc == 'BuyablePower':
            return self.BuyablePower
        else:
            raise Exception("Parsing Error; ability.py")

