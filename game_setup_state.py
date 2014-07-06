__author__ = 'JordSti'
import gui
import cards


class game_setup_state(gui.gui_state):
    # need todo
    # combobox to pick superhero
    # check box for all random
    # duplicated hero ?
    def __init__(self):
        gui.gui_state.__init__(self)

        #loading superheroes

        self.library = cards.library("../dc-deck/pack1")

        self.lbl_title = gui.label()
        self.lbl_title.font = gui.get_big_font()
        self.lbl_title.text = "Game Setup"

        self.lbl_players_name = gui.label()
        self.lbl_players_name.text = "Players name"

        self.lbl_players_num = gui.label()
        self.lbl_players_num.text = "Number of players : "
        self.lbl_players_num.render()

        self.cb_players_num = gui.combobox(50, 22)
        self.cb_players_num.items.append("2")
        self.cb_players_num.items.append("3")
        self.cb_players_num.items.append("4")
        self.cb_players_num.items.append("5")
        self.cb_players_num.add_receiver(self.player_num_changed)

        self.lbl_cb_superhero_pick = gui.label()
        self.lbl_cb_superhero_pick.text = "Random superhero : "

        self.cb_superhero_pick = gui.checkbox()
        self.cb_superhero_pick.checked = True
        self.cb_superhero_pick.state_changed = self.pick_random_changed

        self.add(self.lbl_title)
        self.add(self.lbl_players_name)

        self.add(self.lbl_players_num)
        self.add(self.cb_players_num)

        self.add(self.lbl_cb_superhero_pick)
        self.add(self.cb_superhero_pick)

        self.tb_players = []
        self.lbl_players = []
        self.slider_player_superhero = []
        nb_players = int(self.cb_players_num.get_item())
        for i in range(5):
            tb = gui.textbox(180, 22)
            self.tb_players.append(tb)
            self.add(tb)
            lbl = gui.label(25, 22)
            lbl.text = str(i+1) + " : "
            self.lbl_players.append(lbl)
            self.add(lbl)

            if i < nb_players:
                tb.visible = True
                lbl.visible = True
            else:
                tb.visible = False
                lbl.visible = False

            #todo
            #slider would be a better choice for this
            slider = gui.slider(100, 22)
            slider.visible = False
            #cb.dropdown_height = 190
            for s in self.library.superheroes:
                slider.items.append(s.name)

            self.slider_player_superhero.append(slider)

            self.add(slider)

        self.btn_start = gui.button(180, 40)
        self.btn_start.caption = "Start !"
        self.btn_start.add_receivers(self.start_game)

        self.btn_back = gui.button(180, 40)
        self.btn_back.caption = "Back"
        self.btn_back.add_receivers(self.back)

        self.add(self.btn_start)
        self.add(self.btn_back)

    def player_num_changed(self, src, nb_players):
        nb_players = int(nb_players)
        for i in range(5):
            if i < nb_players:
                self.tb_players[i].visible = True
                self.lbl_players[i].visible = True
                if not self.cb_superhero_pick.checked:
                    self.slider_player_superhero[i].visible = True
            else:
                self.tb_players[i].visible = False
                self.lbl_players[i].visible = False
                self.slider_player_superhero[i].visible = False

    def pick_random_changed(self, checkbox):
        i = 0
        nb_players = int(self.cb_players_num.get_item())

        for slider in self.slider_player_superhero:
            if i < nb_players:
                slider.visible = not checkbox.checked
            i += 1

    def game_start_check(self):

        nb_players = int(self.cb_players_num.get_item())
        superheroes = []
        for s in self.library.superheroes:
            superheroes.append(s.name)
        if not self.cb_superhero_pick.checked:
            for i in range(nb_players):
                p_superhero = self.slider_player_superhero[i].get_item()
                if p_superhero in superheroes:
                    superheroes.remove(p_superhero)
                else:
                    dialog = gui.dialogbox(self)
                    dialog.caption = "A Superhero can only by pick by one player"
                    dialog.title = "Game error"
                    return False

        return True

    def start_game(self, src):

        if self.game_start_check():
            player_num = int(self.cb_players_num.get_item())
            names = []
            for i in range(player_num):
                pn = self.tb_players[i].text
                names.append(pn)

            from game_state import game_state
            state = game_state(names)
            self.viewport.push(state)

    def back(self, src):
        from main_menu import main_menu
        state = main_menu()
        self.viewport.push(state)

    def init(self):

        self.lbl_title.x = 30
        self.lbl_title.y = 20

        self.btn_back.x = 30
        self.btn_back.y = self.height - 100

        self.btn_start.x = self.width - 300
        self.btn_start.y = self.height - 100

        self.lbl_players_name.x = 20
        self.lbl_players_name.y = 120

        self.lbl_players_num.x = 600
        self.lbl_players_num.y = 200

        self.cb_players_num.x = self.lbl_players_num.x + self.lbl_players_num.width + 5
        self.cb_players_num.y = 200

        self.lbl_cb_superhero_pick.x = 600
        self.lbl_cb_superhero_pick.y = 250
        self.lbl_cb_superhero_pick.render()

        self.cb_superhero_pick.x = self.lbl_cb_superhero_pick.x + self.lbl_cb_superhero_pick.width + 5
        self.cb_superhero_pick.y = 250

        current_y = 150

        for i in range(5):
            self.lbl_players[i].x = 50
            self.lbl_players[i].y = current_y

            self.tb_players[i].x = 75
            self.tb_players[i].y = current_y

            self.slider_player_superhero[i].x = 265
            self.slider_player_superhero[i].y = current_y

            current_y += 30
