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


class ability:
    (Passive, Attack, Defense) = (0, 1, 2)

    def __init__(self, type=Passive):
        self.type = type
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
