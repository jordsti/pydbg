__author__ = 'JordSti'
import card_action


class bonus:
    (Power, CostReduction, DrawCard, NextHandCard) = (0, 1, 2, 3)

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
            elif type == 'NextHandCard':
                self.type = self.NextHandCard

            self.nb = int(data[1])


def get_bonus_type(text):
    if text == 'Power':
        return bonus.Power
    elif text == 'CostReduction':
        return bonus.CostReduction
    elif text == 'DrawCard':
        return bonus.DrawCard
    elif text == 'NextHandCard':
        return bonus.NextHandCard

    return None


class condition:
    (MinCard, ForEach, MinCost, EmptyDiscardPile, FirstPlayed, ForEachDifferentName, ActionCompleted) = (0, 1, 2, 3, 4, 5, 6)
    (CardType, CardName, CardCost, CardAbility, CardDifferentNameCount) = (0, 1, 2, 3, 4)
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
        nb_vars = len(data)
        if nb_vars >= 1:
            #condition
            cond = data[0].rstrip(':')
            if cond == 'MinCard':
                self.cond = self.MinCard
            elif cond == 'ForEach':
                self.cond = self.ForEach
            elif cond == 'MinCost':
                self.cond = self.MinCost
            elif cond == 'EmptyDiscardPile':
                self.cond = self.EmptyDiscardPile
            elif cond == 'FirstPlayed':
                self.cond = self.FirstPlayed
            elif cond == 'ForEachDifferentName':
                self.cond = self.ForEachDifferentName
            elif cond == 'ActionCompleted':
                self.cond = self.ActionCompleted

        if nb_vars >= 2:
            #test var
            test = data[1].rstrip(':')

            if test == 'CardType':
                self.test = self.CardType
            elif test == 'CardName':
                self.test = self.CardName
            elif test == 'CardAbility':
                self.test = self.CardAbility
            elif test == 'CardDifferentNameCount':
                self.test = self.CardDifferentNameCount
            elif test == 'CardCost':
                self.test = self.CardCost

        if nb_vars >= 3:
            #where
            where = data[2].rstrip(':')

            if where == 'DiscardPile':
                self.where = self.DiscardPile
            elif where == 'PlayedCard':
                self.where = self.PlayedCard
            elif where == 'LineUp':
                self.where = self.LineUp
            elif where == 'DeckTopCard':
                self.where = self.DeckTopCard
            elif where == 'GainedCard':
                self.where = self.GainedCard

        if nb_vars >= 4:
            #value
            if '|' in data[3]:
                self.value = data[3].split('|')
            else:
                self.value = [data[3]]

        if nb_vars >= 5:
            #count
            self.count = int(data[4])


class ability:
    (Passive, Attack, Defense, EndOfTurn) = (0, 1, 2, 3)

    def __init__(self, type=Passive):
        self.type = type
        self.conditions = []  # todo need to rework this
        self.condition = None
        self.pre_conditions = []
        self.bonus = None
        self.bonuses = [] # todo need rework on this too
        self.action = None

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
                elif type == 'EndOfTurn':
                    self.type = self.EndOfTurn
            elif d.startswith("bonus:"):
                bon = d[6:]
                b = bonus()
                b.from_string(bon)
                self.bonuses.append(b)
                self.bonus = b

            elif d.startswith("condition:"):
                cond = d[10:]
                c = condition()
                c.from_string(cond)
                self.conditions.append(c)

                self.condition = c

            elif d.startswith("action:"):
                action = d[7:]
                a = card_action.card_action()
                a.from_string(action)
                self.action = a
                print "[DEBUG] Ability Constraint Count %d" % len(self.action.constraints), a
                for c in self.action.constraints:
                    print "[DEBUG]", c

class superhero_bonus:
    def __init__(self, superhero, ability, bonus):
        self.superhero = superhero
        self.ability = ability
        self.bonus = bonus
        self.applied = False