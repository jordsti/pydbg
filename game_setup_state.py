__author__ = 'JordSti'
import gui


class game_setup_state(gui.gui_state):

    def __init__(self):
        gui.gui_state.__init__(self)

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

        self.add(self.lbl_title)
        self.add(self.lbl_players_name)

        self.add(self.lbl_players_num)
        self.add(self.cb_players_num)

        self.tb_players = []
        self.lbl_players = []
        for i in range(5):
            tb = gui.textbox(180, 22)
            self.tb_players.append(tb)
            self.add(tb)
            lbl = gui.label(25, 22)
            lbl.text = str(i+1) + " : "
            self.lbl_players.append(lbl)
            self.add(lbl)

        self.btn_start = gui.button(180, 40)
        self.btn_start.caption = "Start !"
        self.btn_start.add_receivers(self.start_game)

        self.btn_back = gui.button(180, 40)
        self.btn_back.caption = "Back"
        self.btn_back.add_receivers(self.back)

        self.add(self.btn_start)
        self.add(self.btn_back)

    def start_game(self, src):

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

        self.lbl_players_num.x = 400
        self.lbl_players_num.y = 200

        self.cb_players_num.x = self.lbl_players_num.x + self.lbl_players_num.width + 5
        self.cb_players_num.y = 200

        current_y = 150

        for i in range(5):
            self.lbl_players[i].x = 50
            self.lbl_players[i].y = current_y

            self.tb_players[i].x = 75
            self.tb_players[i].y = current_y
            current_y += 30
