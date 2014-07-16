__author__ = 'JordSti'

import gui
import main_menu
import sys
import os
import logger

if __name__ == '__main__':
    #python deck build game
    #pydbg for mate

    #todo fullscreen support can be interesting

    #args parsing
    width = 1200
    height = 680

    #window position
    os.environ['SDL_VIDEO_WINDOW_POS'] = "10,30"

    i = 0
    nargs = len(sys.argv)
    while i < nargs:
        arg = sys.argv[i]

        if arg == '-w' or arg == '--width':
            i += 1
            if i < nargs:
                width = int(sys.argv[i])
        elif arg == '-h' or arg == '--height':
            i += 1
            if i < nargs:
                height = int(sys.argv[i])
        elif arg == '-r' or arg == 'resolution':
            i += 1
            if i < nargs:
                res = sys.argv[i]
                data = res.split('x')
                if len(data) == 2:
                    width = int(data[0])
                    height = int(data[1])
        elif arg == '-d' or arg == '--debug':
            logger.set_output_level(logger.logger.Debug)
            print "Debug Output, Have fun !"
        elif arg == '-v' or arg == '--verbose':
            logger.set_output_level(logger.logger.Verbose)

        i += 1

    print "Python Deck Building Game"
    print "Opening window [%dx%d]" % (width, height)

    style = gui.get_style()

    viewport = gui.create_viewport(width, height)

    state = main_menu.main_menu()

    viewport.push(state)
