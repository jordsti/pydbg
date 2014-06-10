__author__ = 'JordSti'

import gui
import main_menu

if __name__ == '__main__':

    viewport = gui.create_viewport(1200, 680)

    state = main_menu.main_menu()

    viewport.push(state)
