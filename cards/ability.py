__author__ = 'JordSti'


class bonus:
    (Power, CostReduction, DrawCard) = (0, 1, 2)

    def __init__(self, type=Power, nb=0):
        self.type = type
        self.nb = nb

    def from_string(self, text):

        data = text.split(':')

        if len(data) >= 2:
            type = data[0].rstrip(':')
            if type == 'Power':
                self.type = self.Power
            elif type == 'CostReduction':
                self.type = self.CostReduction
            elif type == 'DrawCard':
                self.type = self.DrawCard

            self.nb = int(data[1])


class condition:
    (MinCard, ForEach, MinCost) = (0, 1, 2)
    (CardType, CardName, CardCost) = (0, 1, 2)
    (DiscardPile, PlayedCard, LineUp, DeckTopCard, GainedCard) = (0, 1, 2, 3, 4)

    def __init__(self, cond=MinCost, where=PlayedCard, value=""):
        self.cond = cond
        self.where = where

        if '|' in value:
            self.value = value.split('|')
        else:
            self.value = [value]

        self.count = 0
        self.test = self.CardType
        self.inner_condition = None

    def from_string(self, text):
        data = text.split(':')
        if len(data) >= 3:
            cond = data[0].rstrip(':')
            if cond == 'MinCard':
                self.cond = self.MinCard
            elif cond == 'ForEach':
                self.cond = self.ForEach
            elif cond == 'MinCost':
                self.cond = self.MinCost

            test = data[1].rstrip(':')

            if test == 'CardType':
                self.test = self.CardType

            where = data[2].rstrip(':')

            if where == 'DiscardPile':
                self.where = self.DiscardPile
            elif where == 'PlayedCard':
                self.where = self.PlayedCard
            elif where == 'LineUp':
                self.where = self.LineUp
            elif where == 'DeckTopCard':
                self.where = self.DeckTopCard

            if len(data) >= 4:
                self.value = data[3]

            if len(data) >= 5:
                self.count = int(data[4])

class ability:
    (Passive, Attack, Defense) = (0, 1, 2)

    def __init__(self, type=Passive):
        self.type = type
        self.conditions = []
        self.pre_conditions = []
        self.bonus = []

    def from_string(self, text):
        data = text.split(',')

        for d in data:
            d = d.rstrip(',')
            if d.startswith("type:"):
                type = d[5:]
                if type == 'Passive':
                    self.type = self.Passive
                elif type == 'Attack':
                    self.type = self.Attack
                elif type == 'Defense':
                    self.type = self.Defense
            elif d.startswith("bonus:"):
                bon = d[6:]
                b = bonus()
                b.from_string(bon)
                self.bonus.append(b)
            elif d.startswith("condition:"):
                cond = d[10:]
                c = condition()
                c.from_string(cond)

                self.conditions.append(c)
