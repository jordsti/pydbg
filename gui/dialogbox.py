__author__ = 'JordSti'
from widget import widget
from button import button
import font
import pygame


class dialogbox(widget):

    (DefaultWidth, DefaultHeight) = (320, 200)
    (Ok, OkCancel) = (1, 2)
    (ButtonOk, ButtonCancel) = (1, 2)

    def __init__(self, parent, title="", caption="", buttons=Ok, width=0, height=0, auto_spawn=True):
        widget.__init__(self, 'dialogbox', width, height)

        self.auto_spawn = auto_spawn

        self.button_width = 60
        self.button_height = 20
        self.button_offset = 10

        self.title_bar_height = 20

        self.font = font.get_font()
        self.buttons = buttons

        self.__buttons = []

        self.parent = parent

        if self.width == 0 and self.height == 0:
            #applying default dimension
            self.width = self.DefaultWidth
            self.height = self.DefaultHeight

        self.caption = caption
        self.title = title

        self.dialog_action = None
        self.__generate_buttons()

        if self.auto_spawn:
            self.spawn()

    def spawn(self):
        self.x = (self.parent.width - self.width) / 2
        self.y = (self.parent.height - self.height) / 2
        self.parent.pop_dialog(self)

    def __generate_buttons(self):

        if self.buttons == self.Ok:
            btn_ok = button(self.button_width, self.button_height)
            btn_ok.caption = "Ok"
            btn_ok.add_receivers(self.__ok)
            btn_ok.x = (self.width - self.button_width) / 2
            btn_ok.y = (self.height - self.button_height) - self.button_offset
            self.__buttons.append(btn_ok)

        elif self.buttons == self.OkCancel:
            btn_ok = button(self.button_width, self.button_height)
            btn_ok.caption = "Ok"
            btn_ok.add_receivers(self.__ok)
            btn_ok.x = ((self.width - self.button_width*2) / 2) - self.button_offset
            btn_ok.y = (self.height - self.button_height) - self.button_offset
            self.__buttons.append(btn_ok)

            btn_cancel = button(self.button_width, self.button_height)
            btn_cancel.caption = "Cancel"
            btn_cancel.add_receivers(self.__cancel)
            btn_cancel.x = btn_ok.x + btn_ok.width + self.button_offset
            btn_cancel.y = btn_ok.y
            self.__buttons.append(btn_cancel)

    def on_click(self, button, rel_x, rel_y):
        for btn in self.__buttons:
            if btn.contains(rel_x, rel_y):
                rel_x = rel_x - btn.x
                rel_y = rel_y - btn.y
                btn.on_click(button, rel_x, rel_y)

    def on_mouse_over(self, rel_x, rel_y):
        for btn in self.__buttons:
            if btn.contains(rel_x, rel_y):
                btn.hover = True
            else:
                btn.hover = False

    def __ok(self, src):
        self.parent.remove_dialog()
        if self.dialog_action is not None:
            self.dialog_action(self, self.ButtonOk)

    def __cancel(self, src):
        self.parent.remove_dialog()
        if self.dialog_action is not None:
            self.dialog_action(self, self.ButtonCancel)

    def render(self):
        buffer = pygame.Surface((self.width, self.height))

        #dialog border
        rect = pygame.Rect(0, 0, self.width, self.height)

        buffer.fill(self.background_color)
        pygame.draw.rect(buffer, self.foreground_color, rect, 1)

        #title bar
        rect.h = self.title_bar_height
        pygame.draw.rect(buffer, self.foreground_color, rect, 1)

        text = self.font.render(self.title, True, self.foreground_color)

        rect.x = 5
        rect.y = (self.title_bar_height - text.get_height())/2
        rect.w = text.get_width()
        rect.h = text.get_height()

        buffer.blit(text, rect)

        #text caption

        text = self.font.render(self.caption, True, self.foreground_color)

        rect.x = 5
        rect.y = self.title_bar_height + 20
        rect.w = text.get_width()
        rect.h = text.get_height()

        buffer.blit(text, rect)

        #buttons

        for btn in self.__buttons:
            sur = btn.render()
            rect = btn.get_rect()

            buffer.blit(sur, rect)

        return buffer
