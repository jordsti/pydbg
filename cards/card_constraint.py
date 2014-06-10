__author__ = 'JordSti'
from constraint import constraint


class card_constraint(constraint):

    (Cost, Power, Type) = (0, 1, 2)
    (Max, Min, Equals) = (0, 1, 2)

    def __init__(self, var=Type, value="STARTER", test=Equals):
        constraint.__init__(self, "card_constraint")
        self.test = test
        self.value = value
        self.var = var

    def from_string(self, text):
        vars = text.split('-')
        nb_vars = len(vars)

        if nb_vars >= 1:
            #var
            if vars[0] == 'Cost':
                self.var = self.Cost
            elif vars[0] == 'Power':
                self.var = self.Power
            elif vars[0] == 'Type':
                self.var = self.Type

        if nb_vars >= 2:
            #value
            self.value = vars[1]

        if nb_vars >= 3:
            #test
            if vars[2] == 'Min':
                self.test = self.Min
            elif vars[2] == 'Max':
                self.test = self.Max
            elif vars[2] == 'Equals':
                self.test = self.Equals

    def pass_condition(self, obj):
        if self.var == self.Cost:
            cost = int(self.value)
            if self.test == self.Max:
                if obj.cost <= cost:
                    return True
            elif self.test == self.Min:
                if obj.cost >= cost:
                    return True
            elif self.test == self.Equals:
                if obj.cost == cost:
                    return True
        elif self.var == self.Type:
            #only equals is handled !!

            if obj.card_type == self.value:
                return True
        elif self.var == self.Power:
            pass
            #todo

        return False

