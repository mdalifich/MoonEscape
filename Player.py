import os
import sys
from operator import itemgetter
from random import randint, choice
import pygame
from pygame import *
from MatClasses import *
from Glob import *


class Person(Animated, pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.animList = ['Icons/person1.png', 'Icons/person2.png', 'Icons/person3.png', 'Icons/person4.png',
                         'Icons/person5.png']
        self.hp = 5
        self.weapon = 0
        self.image = load_image(self.animList[0]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (42, 64))
        self.mask = pygame.mask.from_surface(self.image)
        self.scale = (42, 64)
        self.x = 300
        self.y = 300
        self.rect = Rect(self.x, self.y, 42, 64)
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def jump(self):
        if self.rect.y == 300:
            self.rect.y -= 200
        elif self.rect.y >= 20:
            self.rect.y -= 10

    def fall(self):
        self.rect.y += 10
