import os
import sys
from operator import itemgetter
from random import randint, choice
import pygame
from pygame import *
from MatClasses import *


class Background(Mov, pygame.sprite.Sprite):
    def __init__(self, x, y, screen, sel, icon):
        super().__init__()
        self.x, self.y = x, y
        self.DiedX = -1000
        self.image = load_image(icon) #'Icons/BackGround.png')
        self.rect = Rect(self.x, self.y, 1000, 400)
        self.selected_option = sel
        self.screen = screen
        self.NoiceSpeed()

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def Die(self):
        self.rect.x = 2000


class BB(Mov, pygame.sprite.Sprite):
    def __init__(self, x, y, opt, screen, icon):
        super().__init__()
        self.x, self.y = x, y
        self.speed = 1
        self.DiedX = -1000
        self.selected_option = opt
        self.iconList = icon # {'Легкая сложность': 'Icons/BBackground.png', 'Нормальная сложность': 'Icons/fon2.png', 'Сложная сложность': 'Icons/fon3.png', 'Non real': 'Icons/Fon1.png'}
        if icon == 'Icons/fonKolobok.png':
            self.image = load_image(self.iconList)
        else:
            self.image = load_image(self.iconList[self.selected_option])
        self.rect = Rect(self.x, self.y, 1000, 274)
        self.screen = screen

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def Die(self):
        self.rect.x = 2000

    def Moving(self):
        self.rect.x -= self.speed
        if self.rect.x <= self.DiedX:
            self.Die()


class Platforms(Mov, pygame.sprite.Sprite):
    def __init__(self, screen, sel, icon):
        super().__init__()

        self.DiedX = -2405
        self.image = load_image(icon) #'Icons/platform.png').convert_alpha()
        self.n = randint(15, 80)
        self.mask = pygame.mask.from_surface(self.image)
        self.y = randint(150, 250)
        self.x = 1000
        self.rect = Rect(self.x, self.y, 96, 32)
        self.selected_option = sel
        self.screen = screen
        self.NoiceSpeed()

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))

    def Die(self):
        self.kill()


class Money(Animated, Mov, pygame.sprite.Sprite):
    def __init__(self, screen, sel):
        super().__init__()
        self.animList = ['Icons/Money.png', 'Icons/Money2.png', 'Icons/Money3.png', 'Icons/Money4.png', 'Icons/Money5.png', 'Icons/Money6.png']
        self.Collid = False
        self.AnimCount = 0
        self.y = randint(150, 280)
        self.x = 1000
        self.DiedX = -2405
        self.image = load_image(self.animList[0])
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = Rect(self.x, self.y, 24, 24)
        self.selected_option = sel
        self.screen = screen
        self.NoiceSpeed()

    def Die(self):
        self.kill()

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.AnimCount += 1
        if self.AnimCount > 50:
            self.AnimCount = 0
        if self.AnimCount % 10 == 0:
            self.AnimationUpdate(self.AnimCount // 10)


class Card(Animated, Mov, pygame.sprite.Sprite):
    def __init__(self, screen, sel):
        super().__init__()
        self.animList = ['Icons/Card.png', 'Icons/Card2.png', 'Icons/Card3.png', 'Icons/Card4.png', 'Icons/Card5.png', 'Icons/Card6.png', 'Icons/Card7.png', 'Icons/Card8.png']
        self.Collid = False
        self.AnimCount = 0
        self.y = randint(150, 280)
        self.x = 2000
        self.DiedX = -130
        self.image = load_image(self.animList[0])
        self.image = pygame.transform.scale(self.image, (24, 24))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = Rect(self.x, self.y, 24, 24)
        self.DieFlag = False
        self.selected_option = sel
        self.screen = screen
        self.NoiceSpeed()

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.AnimCount += 1
        if self.AnimCount > 70:
            self.AnimCount = 0
        if self.AnimCount % 10 == 0:
            self.AnimationUpdate(self.AnimCount // 10)


class Door(Animated, Mov, pygame.sprite.Sprite):
    def __init__(self, screen, sel):
        super().__init__()
        self.OpenTheDoors = None
        self.animList = ['Icons/Entry.png', 'Icons/Entry2.png', 'Icons/Entry3.png', 'Icons/Entry4.png', 'Icons/Entry5.png']
        self.AnimCount = 0
        self.y = 62
        self.x = 2500
        self.die = False
        self.DiedX = -130
        self.image = load_image(self.animList[0])
        self.image = pygame.transform.scale(self.image, (128, 274))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = Rect(self.x, self.y, 128, 274)
        self.selected_option = sel
        self.screen = screen
        self.NoiceSpeed()
        self.MasterCard = Card(self.screen, self.selected_option)


    def Die(self):
        self.rect.x = randint(2500, 4000)
        self.AnimCount = 0
        self.image = load_image(self.animList[0])
        self.image = pygame.transform.scale(self.image, (128, 274))
        self.MasterCard.Collid = False
        self.OpenTheDoors = False
        self.die = True

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.MasterCard.draw()
        self.MasterCard.Moving()
        if self.MasterCard.Collid:
            self.OpenTheDoors = True
            if self.AnimCount < 40:
                self.AnimCount += 1
            if self.AnimCount % 10 == 0:
                self.AnimationUpdate(self.AnimCount // 10)
                self.image = pygame.transform.scale(self.image, (128, 274))

        if not self.OpenTheDoors or self.die:
            self.MasterCard.rect.x = self.rect.x - 250
            self.die = False
        self.MasterCard.y = randint(150, 280)