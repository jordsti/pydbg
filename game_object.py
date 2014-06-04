__author__ = 'JordSti'
import player
import random
import cards


class lineup_action:
    (Added, Removed) = (0, 1)

    def __init__(self, card, type=Added):
        self.card = card
        self.type = type


class game_object:

    def __init__(self, library):
        self.players = []
        self.player_count = 0
        self.library = library
        self.starting_player = None
        self.current_player = None
        self.turns = 0
        self.lineups = []

        self.buyable_powers = []
        self.curses = []

        self.main_deck = cards.card_deck()

        self.change_turn = None
        self.card_played = None
        self.lineup_changed = None

    def buy_card(self, card):
        current = self.get_current_player()
        if card in self.lineups:
            if card.cost <= current.total_power:
                current.total_power -= card.cost
                self.lineups.remove(card)
                current.gained_cards.append(card)

                if self.lineup_changed is not None:
                    actions = [lineup_action(card, lineup_action.Removed)]
                    self.lineup_changed(actions)

        elif card in self.buyable_powers:
            if card.cost <= current.total_power:
                current.total_power -= card.cost
                self.buyable_powers.remove(card)
                current.gained_cards.append(card)

    def end_turn(self):
        current = self.get_current_player()

        gained_cards = current.gained_cards

        played_cards = current.played_cards

        current.gained_cards = []
        current.played_cards = []

        for p in played_cards:
            current.discard_pile.append(p)

        for g in gained_cards:
            current.discard_pile.append(g)

        #pick new hand

        if len(current.hand) > 0:
            for c in current.hand:
                current.discard_pile.append(c)
            current.hand = []

        nb = current.next_hand_size

        for i in range(nb):
            if not current.deck.empty():
                c = current.deck.pop()
                current.hand.append(c)
            else:
                for c in current.discard_pile:
                    current.deck.push(c)

                current.discard_pile = []

                current.deck.shuffle()
                c = current.deck.pop()
                current.hand.append(c)

        #fill lineups
        actions = []
        while len(self.lineups) < 5 and not self.main_deck.empty():
            card = self.main_deck.pop()
            self.lineups.append(card)
            actions.append(lineup_action(card, lineup_action.Added))

        if len(actions) > 0:
            if self.lineup_changed is not None:
                self.lineup_changed(actions)

        #changing turn
        current.is_playing = False
        self.change_player_turn()

    def change_player_turn(self):

        self.current_player += 1

        if self.current_player >= len(self.players):
            self.current_player %= len(self.players)

        current = self.get_current_player()
        current.is_playing = True
        current.total_power = 0

        if self.current_player == self.starting_player:
            self.turns += 1
            print "Turn complete %d " % self.turns
        if self.change_turn is not None:
            self.change_turn(current)

    def get_current_player(self):
        return self.players[self.current_player]

    def play_card(self, player, card):
        if player == self.get_current_player():
            if card in player.hand:
                player.played_cards.append(card)

                if self.card_played is not None:
                    self.card_played(player, card)

                player.hand.remove(card)
                self.apply_card(card)
            else:
                print "Error 2"
        else:
            print "Error 1"

    def apply_card(self, card):
        player = self.get_current_player()
        for a in card.abilities:
            if len(a.pre_conditions) == 0:
                if a.type == cards.ability.Passive:
                    for b in a.bonus:
                        if b.type == cards.bonus.Power:
                            player.total_power += b.nb

    def create_cards(self):

        #buyable power
        nb = 16

        for i in range(nb):
            card_id = self.library.get_card_by_name(self.library.buyable_power)
            gcard = cards.game_card(card_id, self.library)
            self.buyable_powers.append(gcard)

        #curses
        nb = 20
        for i in range(nb):
            card_id = self.library.get_card_by_name(self.library.curse_card)
            ccard = cards.game_card(card_id, self.library)
            self.curses.append(ccard)

        #generating main deck
        for k in self.library.cards_count:
            nb = self.library.cards_count[k]
            card_id = self.library.get_card_by_name(k)

            for i in range(nb):
                try:
                    gcard = cards.game_card(card_id, self.library)
                    self.main_deck.push(gcard)
                except AttributeError as e:
                    print e.message, k

        self.main_deck.shuffle(1000)

        #starter for each player
        starters = self.library.get_starter()
        for p in self.players:
            for c_id in starters:
                gcard = cards.game_card(c_id, self.library)
                p.deck.push(gcard)

            p.deck.shuffle()

            for c in range(5):
                c = p.deck.pop()
                p.hand.append(c)

        #line up
        for i in range(5):
            self.lineups.append(self.main_deck.pop())

    def start_game(self):
        self.turns += 1
        if self.change_turn is not None:
            player = self.get_current_player()
            player.is_playing = True
            self.change_turn(player)

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
