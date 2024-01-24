import os
import sys
from operator import itemgetter
from random import randint, choice
import pygame
from pygame import *
from Glob import *


def draw_text(wind, text, x, y):
    font = pygame.font.Font(None, 50)
    text_surface = font.render(text, True, (255, 0, 0))
    wind.blit(text_surface, (x, y))


def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Mov(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.step = 0
        self.speed = 0
        self.x = 0
        self.y = 0
        self.DiedX = -200
        self.rect = Rect(0, 0, 1, 1)

    def NoiceSpeed(self):
        if self.selected_option == 'Легкая сложность':
            self.speed = 5
        elif self.selected_option == 'Нормальная сложность':
            self.speed = 10
        elif self.selected_option == 'Сложная сложность':
            self.speed = 15
        elif self.selected_option == 'Non real':
            self.speed = 20
        self.step = 0

    def Die(self):
        pass

    def Moving(self):
        self.rect.x -= self.speed
        if self.rect.x <= self.DiedX:
            self.Die()
        self.step += 1


class Animated(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animList = ['Icons/Box1.png']
        self.image = None
        self.scale = (50, 50)

    def AnimationUpdate(self, i):
        self.image = load_image(self.animList[i])
        self.image = pygame.transform.scale(self.image, self.scale)