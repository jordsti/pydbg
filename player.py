__author__ = 'JordSti'
import cards


class player:

    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.superhero = None

        self.discard_pile = []

        self.deck = cards.card_deck()
