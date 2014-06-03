__author__ = 'JordSti'

import gui


class main_menu(gui.gui_state):

    def __init__(self):
        gui.gui_state.__init__(self)

        self.btn_width = 180
        self.btn_height = 35

        self.btn_offset = 15

        self.title = gui.label()
        self.btn_new_game = gui.button(self.btn_width, self.btn_height)
        self.btn_deck_view = gui.button(self.btn_width, self.btn_height)
        self.btn_quit = gui.button(self.btn_width, self.btn_height)

    def init(self):

        self.title.font = gui.get_big_font()

        self.title.text = "Py Deck Building Game"

        self.title.render()

        self.title.x = (self.width - self.title.width) / 2
        self.title.y = 20

        self.btn_new_game.caption = "New Game"
        self.btn_new_game.x = (self.width - self.btn_width) / 2
        self.btn_new_game.y = self.title.y + self.title.height + self.btn_offset
        self.btn_new_game.add_receivers(self.new_game)

        self.btn_deck_view.caption = "View Deck"
        self.btn_deck_view.x = (self.width - self.btn_width) / 2
        self.btn_deck_view.y = self.btn_new_game.y + self.btn_height + self.btn_offset
        self.btn_deck_view.add_receivers(self.deck_view)

        self.btn_quit.caption = "Quit"
        self.btn_quit.x = (self.width - self.btn_width) / 2
        self.btn_quit.y = self.btn_deck_view.y + self.btn_height + self.btn_offset
        self.btn_quit.add_receivers(self.quit)

        self.add(self.title)
        self.add(self.btn_new_game)
        self.add(self.btn_deck_view)
        self.add(self.btn_quit)

    def new_game(self, src):
        from game_setup_state import game_setup_state
        state = game_setup_state()
        self.viewport.push(state)

    def deck_view(self, src):
        import deck_view
        state = deck_view.deck_view()
        self.viewport.push(state)

    def quit(self, src):
        self.viewport._run = False