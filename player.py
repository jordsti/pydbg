__author__ = 'JordSti'
import cards


class player:

    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.superhero = None
        self.passive_superhero = False
        self.next_hand_size = 5
        self.discard_pile = []
        self.played_cards = []

        self.gained_cards = []

        self.total_power = 0

        self.deck = cards.card_deck()

        self.is_playing = False

        self.hand = []