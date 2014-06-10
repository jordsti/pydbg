__author__ = 'JordSti'


class constraint:

    def __init__(self, name="NotSet"):
        self.name = name

    def from_string(self, text):
        #not handled by superclass
        pass

    def pass_condition(self, obj):
        #to be implemented
        return False