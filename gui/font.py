__author__ = 'JordSti'

import pygame

default_font = None

big_font = None


def get_big_font():

    global big_font

    if big_font is None:
        f = pygame.font.Font(pygame.font.get_default_font(), 24)

        big_font = f

    return big_font


def get_font():

    global default_font

    if default_font is None:

        f = pygame.font.Font(pygame.font.get_default_font(), 12)

        default_font = f

    return default_font