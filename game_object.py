__author__ = 'JordSti'
import player
import random
import cards


class game_object:

    def __init__(self, library):
        self.players = []
        self.player_count = 0
        self.library = library
        self.starting_player = None
        self.current_player = None

        self.lineups = []

        self.buyable_powers = []
        self.curses = []

        self.main_deck = cards.card_deck()

    def create_cards(self):

        #buyable power
        nb = 16

        for i in range(nb):
            card_id = self.library.get_card_by_name(self.library.buyable_power)
            gcard = cards.game_card(card_id)
            self.buyable_powers.append(gcard)

        #curses
        nb = 20
        for i in range(nb):
            card_id = self.library.get_card_by_name(self.library.curse_card)
            ccard = cards.game_card(card_id)
            self.curses.append(ccard)

        #generating main deck
        for k in self.library.cards_count:
            nb = self.library.cards_count[k]
            card_id = self.library.get_card_by_name(k)

            for i in range(nb):
                try:
                    gcard = cards.game_card(card_id)
                    self.main_deck.push(gcard)
                except AttributeError as e:
                    print e.message, k

        self.main_deck.shuffle(1000)

        #starter for each player
        starters = self.library.get_starter()
        for p in self.players:
            for c_id in starters:
                gcard = cards.game_card(c_id)
                p.deck.push(gcard)

            p.deck.shuffle()

        #line up

        for i in range(5):
            self.lineups.append(self.main_deck.pop())

    def add_player(self, name):
        p = player.player(self.player_count, name)
        self.player_count += 1
        self.players.append(p)

    def get_player_index(self, player):

        index = 0
        for p in self.players:
            if p == player:
                return index
            index += 1

        return -1

    def get_player(self, name):

        for p in self.players:
            if p.name == name:
                return p

        return None

    def pick_superhero(self):

        players_roll = {}

        for p in self.players:
            roll = random.randint(0, 100)
            players_roll[p.name] = roll

        winner = self.players[0]
        max = players_roll[winner.name]

        for k in players_roll:
            v = players_roll[k]
            if v > max:
                max = v
                winner = self.get_player(k)


        index = self.get_player_index(winner)

        self.starting_player = index
        self.current_player = index

        for i in range(len(self.players)):
            p_i = (index + i) % len(self.players)

            player = self.players[p_i]

            s_i = random.randint(0, len(self.library.superheroes) - 1)

            superhero = self.library.superheroes[s_i]

            player.superhero = superhero

            self.library.superheroes.remove(superhero)
