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
        self.drawn_card = None
        self.ask_player = None

        self.player_choices = []
        self.pending_choice = None

        self.supervilains = cards.card_deck()
        self.current_supervilain = None

    def buy_card(self, card):
        current = self.get_current_player()
        if card in self.lineups:
            if card.cost <= current.total_power:
                current.total_power -= card.cost
                print "buying card from field"
                self.lineups.remove(card)
                current.gained_cards.append(card)

                if self.lineup_changed is not None:
                    actions = [lineup_action(card, lineup_action.Removed)]
                    self.lineup_changed(actions)

                return True

        elif card in self.buyable_powers:
            if card.cost <= current.total_power:
                current.total_power -= card.cost
                print "buying kick"
                self.buyable_powers.remove(card)
                current.gained_cards.append(card)
                return True

        return False

    def end_turn_phase(self):
        #for wonderwoman specially
        #need to split between end_turn_phase, todo like aquaman's trident and other...
        self.end_turn_abilities()
        self.apply_superhero_bonus()

        if self.pending_choice is None:
            #no choice to take !
            self.end_turn()

    def end_turn(self):

        current = self.get_current_player()

        #current.passive_superhero = False # not needed anymore, superhero abilities reworked
        #current.superhero_bonuses = []

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

        current.clean_turn_vars()

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

                #superhero ability check here
                self.superhero_ability_check(card)
                self.apply_superhero_bonus()
            else:
                print "Error 2"
        else:
            print "Error 1"

    def apply_superhero_bonus(self):
        player = self.get_current_player()
        for bonus in player.superhero_bonuses:

            if not bonus.applied:
                if bonus.bonus.type == cards.bonus.Power:
                    player.total_power += bonus.bonus.nb
                elif bonus.bonus.type == cards.bonus.DrawCard:
                    for i in range(bonus.bonus.nb):
                        c = self.draw_player_card(player)
                        player.hand.append(c)

                        if self.drawn_card is not None:
                            self.drawn_card(player, c)
                elif bonus.bonus.type == cards.bonus.NextHandCard:
                    player.next_hand_size += bonus.bonus.nb

                print "Bonus from %s, %d, %d" % (player.superhero.name, bonus.bonus.type, bonus.bonus.nb)
                bonus.applied = True

    def complete_choice(self, choice):
        #todo

        pass

    def end_turn_abilities(self):
        current = self.get_current_player()

        #superhero abilites
        superhero = current.superhero
        #superhero.active check todo
        for a in superhero.abilities:
            if a.type == cards.ability.EndOfTurn:
                if a.condition is not None:
                    if a.condition.cond == cards.condition.ForEach:
                        if a.condition.test == cards.condition.CardType:
                            if a.condition.where == cards.condition.GainedCard:
                                #wonderwoman case
                                for card in current.gained_cards:
                                    if card.card_type in a.condition.value:
                                        sb = cards.superhero_bonus(superhero, a, a.bonus)
                                        current.superhero_bonuses.append(sb)
                else:
                    #aquaman got no condition
                    #superhero only..
                    if a.action is not None:
                        if a.action.type == cards.card_action.ChooseCard:
                            source = None
                            selected_cards = []
                            if a.action.source == cards.card_action.GainedCard:
                                source = current.gained_cards

                            for card in source:
                                if a.action.respect_constraint(card):
                                    selected_cards.append(card)

                            if len(selected_cards) > 0:
                                #the player got to choose
                                dest = None
                                if a.action.destination == cards.card_action.PlayerDeckTop:
                                    dest = player.player_choice.PlayerDeckTop

                                choice = player.player_choice(selected_cards, dest, a.action.count, not a.action.forced)
                                self.player_choices.append(choice)

                                if self.pending_choice is None:
                                    self.pending_choice = choice
                                    if self.ask_player is not None:
                                        self.ask_player(player, choice)

        #card abilities
        #todo

    def superhero_ability_check(self, played_card):
        #starting with martian manhunter case
        player = self.get_current_player()

        if not player.superhero.active:
            return

        for ability in player.superhero.abilities:
            if ability.type == cards.ability.Passive and ability.condition is not None:
                if ability.condition.cond == cards.condition.MinCard:
                    if ability.condition.test == cards.condition.CardType:
                        if ability.condition.where == cards.condition.PlayedCard:
                            #min card with card type, #martian manhunter
                            card_count = 0
                            for c in player.played_cards:
                                if c.card_type == ability.condition.value:
                                    card_count += 1

                            if card_count >= ability.condition.count:
                                sb = cards.superhero_bonus(player.superhero, ability, ability.bonus)

                                if not player.contains_superhero_bonus(sb):
                                    player.superhero_bonuses.append(sb)

                elif ability.condition.cond == cards.condition.FirstPlayed:
                    if ability.condition.test == cards.condition.CardAbility:
                        if ability.condition.where == cards.condition.PlayedCard:
                            #flash case
                            for a in played_card.abilities:
                                if a.bonus is not None:
                                    if a.bonus.type == cards.get_bonus_type(ability.condition.value):

                                        sb = cards.superhero_bonus(player.superhero, ability, ability.bonus)

                                        if not player.contains_superhero_bonus(sb):
                                            player.superhero_bonuses.append(sb)

                    elif ability.condition.test == cards.condition.CardType:
                        if ability.condition.where == cards.condition.PlayedCard:
                            #cybord case
                            if played_card.card_type in ability.condition.value:

                                sb = cards.superhero_bonus(player.superhero, ability, ability.bonus)

                                if not player.contains_superhero_bonus(sb):
                                    player.superhero_bonuses.append(sb)

                elif ability.condition.cond == cards.condition.ForEach:
                    if ability.condition.test == cards.condition.CardType:
                        if ability.condition.where == cards.condition.PlayedCard:
                            if played_card.card_type in ability.condition.value:
                                #batman +1 power for each

                                sb = cards.superhero_bonus(player.superhero, ability, ability.bonus)

                                player.superhero_bonuses.append(sb)
                                #i think existing check is not needed here

                elif ability.condition.cond == cards.condition.ForEachDifferentName:
                    if ability.condition.test == cards.condition.CardType:
                        if ability.condition.where == cards.condition.PlayedCard:

                            #superman case
                            if played_card.card_type in ability.condition.value:
                                #good type
                                unique = True
                                for c in player.played_cards:
                                    if c.name == played_card.name and not c == played_card:
                                        unique = False

                                if unique:
                                    #bonus can apply
                                    sb = cards.superhero_bonus(player.superhero, ability, ability.bonus)
                                    player.superhero_bonuses.append(sb)
                elif ability.condition.cond == cards.condition.MinCost:
                    if ability.condition.test == cards.condition.CardDifferentNameCount:
                        if ability.condition.where == cards.condition.PlayedCard:
                            #green latern
                            min_cost = int(ability.condition.value[0])
                            min_count = ability.condition.count
                            card_names = []

                            for c in player.played_cards:
                                if c.cost >= min_cost:
                                    if c.name not in card_names:
                                        card_names.append(c.name)

                            if len(card_names) >= min_count:
                                #bonus available
                                sb = cards.superhero_bonus(player.superhero, ability, ability.bonus)
                                #only applying once
                                if sb not in player.superhero_bonuses:
                                    player.superhero_bonuses.append(sb)


    def apply_card(self, card):
        player = self.get_current_player()

        for a in card.abilities:
            if a.condition is None:
                if a.type == cards.ability.Passive:
                    print "Bonus from %s, %d, %d" % (card.name, a.bonus.type, a.bonus.nb)
                    if a.bonus.type == cards.bonus.Power:
                        player.total_power += a.bonus.nb
                    elif a.bonus.type == cards.bonus.DrawCard:
                        for i in range(a.bonus.nb):
                            c = self.draw_player_card(player)
                            player.hand.append(c)

                            if self.drawn_card is not None:
                                self.drawn_card(player, c)
            else:
                condition_ok = False
                bonuses = []
                c = a.condition
                if a.type == cards.ability.Passive:
                    if c.cond == cards.condition.MinCard:
                        if c.test == cards.condition.CardType:
                            if c.where == cards.condition.PlayedCard:
                                #high tech hero case
                                count = 0
                                for pcard in player.played_cards:
                                    if pcard.card_type in c.value:
                                        count += 1

                                if count >= c.count:
                                    condition_ok = True

                                    bonuses.append(a.bonus)
                    elif c.cond == cards.condition.EmptyDiscardPile:
                        #mera case
                        if len(player.discard_pile) == 0:
                            condition_ok = True
                            bonuses.append(a.bonus)

                    elif c.cond == cards.condition.MinCost:
                        if c.test == cards.condition.CardCost:
                            if c.where == cards.condition.DeckTopCard:
                                #power ring
                                card = player.deck.reveal()
                                if card.cost >= int(c.value):
                                    bonuses.append(a.bonus)
                                    condition_ok = True

                if condition_ok:
                    for b in bonuses:
                        print "Bonus from %s, %d, %d" % (card.name, b.type, b.nb)
                        if b.type == cards.bonus.Power:
                            player.total_power += b.nb
                        elif b.type == cards.bonus.DrawCard:
                            for i in range(b.nb):
                                c = self.draw_player_card(player)
                                player.hand.append(c)

    def draw_player_card(self, player):
        if player.deck.empty():
            for c in player.discard_pile:
                player.deck.push(c)

            player.deck.shuffle()

        return player.deck.pop()

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

        #supervilain preparation
        first_sv = self.library.get_supervilain_by_name(self.library.first_supervilain)

        first_sv = cards.game_card(first_sv, self.library)

        for sv in self.library.supervilains:
            if not sv == first_sv:
                sv_card = cards.game_card(sv, self.library)
                self.supervilains.push(sv_card)

        #shuffling supervilains
        self.supervilains.shuffle()
        self.supervilains.push(first_sv)
        self.current_supervilain = first_sv

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
