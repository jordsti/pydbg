__author__ = 'JordSti'

import gui
import cards
import main_menu

if __name__ == '__main__':

    lib = cards.library("deck/pack1")

    import game_object

    gom = game_object.game_object(lib)

    gom.add_player("jord sti")
    gom.add_player("josh")
    gom.add_player("john")

    gom.pick_superhero()

    gom.create_cards()



    for c in gom.lineups:
        print c.name, c.image_path

    viewport = gui.create_viewport(800, 600)

    state = main_menu.main_menu()

    viewport.push(state)
