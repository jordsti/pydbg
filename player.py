__author__ = 'JordSti'
import cards


class player:

    def __init__(self, player_id, name):
        self.player_id = player_id
        self.name = name
        self.superhero = None
        self.passive_superhero = False
        self.base_hand_size = 5
        self.next_hand_size = self.base_hand_size
        self.discard_pile = []
        self.played_cards = []

        self.gained_cards = []

        self.total_power = 0

        self.deck = cards.card_deck()

        self.is_playing = False

        self.hand = []

        self.superhero_bonuses = []

    def clean_turn_vars(self):
        self.superhero_bonuses = []
        self.total_power = 0
        self.next_hand_size = self.base_hand_size

    def contains_superhero_bonus(self, superhero_bonus):

        for b in self.superhero_bonuses:
            if b.superhero == superhero_bonus.superhero and b.bonus == superhero_bonus.bonus \
                    and b.ability == superhero_bonus.ability:
                return True

        return False

    def remake_deck(self):

        for c in self.discard_pile:
            self.deck.push(c)

        self.discard_pile = []

        self.deck.shuffle()


class player_choice:
    #todo some text info like which card is resulting in this
    (DiscardCard, DestroyCard, PlayerDeckTop, PlayerDeckBottom, Hand, LineUp, GainedCard) = (0, 1, 2, 3, 4, 5, 6)

    def __init__(self, cards, player, destination=DiscardCard, count=1, may=False, bonus=None):
        self.may = may
        self.player = player
        self.cards = cards
        self.selected_cards = []
        self.count = count
        self.destination = destination
        self.completed = False
        self.bonus = bonus

    def action_completed(self):
        return self.count == len(self.selected_cards)