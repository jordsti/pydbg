__author__ = 'JordSti'

import gui
import pygame


class player_widget(gui.widget):

    def __init__(self, player, width=0, height=0):
        gui.widget.__init__(self, "player_widget", width, height)
        self.player = player
        self.sh_width = 87
        self.sh_height = 118
        self.font = gui.get_font()

        self.superhero_image = pygame.image.load(player.superhero.get_image_path())

        self.superhero_thumb = pygame.transform.scale(self.superhero_image, (self.sh_width, self.sh_height))
        self.playing_border = 0, 250, 0

    def render(self):

        buffer = pygame.Surface((self.width, self.height))

        buffer.fill(self.background_color)

        #border
        border = pygame.Rect(0, 0, self.width, self.height)

        #superhero thumbnail
        dst_rect = pygame.Rect(1, 1, self.sh_width, self.sh_height)

        buffer.blit(self.superhero_thumb, dst_rect)

        #player name

        text = self.font.render(self.player.name, True, self.foreground_color)

        dst_rect.x = 120
        dst_rect.y = 12
        dst_rect.width = text.get_width()
        dst_rect.height = text.get_height()

        buffer.blit(text, dst_rect)

        text = self.font.render(self.player.superhero.name, True, self.foreground_color)

        dst_rect.y = 32
        dst_rect.width = text.get_width()
        dst_rect.height = text.get_height()

        buffer.blit(text, dst_rect)

        text = self.font.render("Hand : %d" % len(self.player.hand), True, self.foreground_color)

        dst_rect.y = 52
        dst_rect.width = text.get_width()
        dst_rect.height = text.get_height()

        buffer.blit(text, dst_rect)

        text = self.font.render("Discard pile : %d" % len(self.player.discard_pile), True, self.foreground_color)

        dst_rect.y = 72
        dst_rect.width = text.get_width()
        dst_rect.height = text.get_height()

        buffer.blit(text, dst_rect)

        if self.player.is_playing:
            text = self.font.render("Power : %d" % self.player.total_power, True, self.foreground_color)

            dst_rect.y = 92
            dst_rect.width = text.get_width()
            dst_rect.height = text.get_height()

            buffer.blit(text, dst_rect)

        if self.player.is_playing:
            pygame.draw.rect(buffer, self.playing_border, border, 2)
        else:
            pygame.draw.rect(buffer, self.foreground_color, border, 1)

        return buffer
