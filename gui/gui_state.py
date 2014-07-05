__author__ = 'JordSti'

from base_state import base_state
import pygame


class gui_state(base_state):

    def __init__(self):
        base_state.__init__(self)

        self.elements = []
        self.__dialog = None

    def bring_to_top(self, element):
        if element in self.elements:
            self.elements.remove(element)
            self.elements.append(element)
        else:
            self.add(element)

    def pop_dialog(self, dialog):
        if self.__dialog is None:
            self.__dialog = dialog

    def remove_dialog(self):
        self.__dialog = None

    def paint(self, screen):

        for e in self.elements:
            if e.visible:
                surface = e.render()

                dst_rect = pygame.Rect(e.x, e.y, e.width, e.height)
                #print e.width, e.height, " %d, %d " % (surface.get_width(), surface.get_height())
                screen.blit(surface, dst_rect)

        if self.__dialog is not None:
            surface = self.__dialog.render()
            rect = self.__dialog.get_rect()
            screen.blit(surface, rect)

    def add(self, element):
        self.elements.append(element)

    def on_event(self, event):

        if event.type == pygame.MOUSEBUTTONUP:
            if self.__dialog is None:
                for e in self.elements:
                    if e.x <= event.pos[0] and e.x + e.width >= event.pos[0] and e.y <= event.pos[1] and e.y + e.height >= event.pos[1]:
                        e.on_click(event.button, event.pos[0] - e.x, event.pos[1] - e.y)
                        #combobox hotfix
                        #todo
                        #find another way to do this !!!

                        if e.widget_name == 'combobox':
                            self.bring_to_top(e)
                            break
                        e.focus = True
                    else:
                        e.focus = False
            else:
                if self.__dialog.contains(event.pos[0], event.pos[1]):
                    self.__dialog.on_click(event.button, event.pos[0] - self.__dialog.x, event.pos[1] - self.__dialog.y)

        elif event.type == pygame.MOUSEMOTION:
            if self.__dialog is None:
                for e in self.elements:
                    if e.x <= event.pos[0] and e.x + e.width >= event.pos[0] and e.y <= event.pos[1] and e.y + e.height >= event.pos[1]:
                        e.is_hover(True)
                    else:
                        e.is_hover(False)
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if self.__dialog is None:
                for e in self.elements:
                    e.on_key(event)

        elif event.type == pygame.QUIT:
            self.viewport._run = False