import os
import sys
from operator import itemgetter
from random import randint, choice
import pygame
from pygame import *
from MatClasses import *
from Glob import *

pygame.mixer.init()

lazerSound = pygame.mixer.Sound('Sounds/Lazer.mp3')


class Bullet(Mov, pygame.sprite.Sprite):
    def __init__(self, typebul, x, y, screen, sel):
        super().__init__()
        self.coef = -6
        self.image = load_image(f'Icons/{typebul}.png')
        self.image = pygame.transform.scale(self.image, (30, 8))
        self.typeBullet = typebul
        self.isAlive = True
        self.DiedX = -1000
        self.x, self.y = x, y
        self.rect = Rect(self.x, self.y, 30, 8)
        self.selected_option = sel
        self.screen = screen
        self.NoiceSpeed()
        self.collide = False

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.Moving()

    def Die(self):
        self.coef = -6
        self.isAlive = False
        lazerSound.play()

    def Moving(self):
        self.rect.x -= self.speed + 10
        if self.typeBullet == 'Arrow':
            self.rect.y += self.coef
        self.coef += 0.25
        if self.rect.x <= self.DiedX:
            self.collide = True
            self.Die()


class Truba(Mov, pygame.sprite.Sprite):
    def __init__(self, screen, sel):
        super().__init__()
        self.barrier = None
        self.image = load_image('Icons/Turba.png')
        self.image = pygame.transform.scale(self.image, (32, 96))
        self.rect = Rect(1000, 0, 32, 96)
        self.count_box = 1
        self.selected_option = sel
        self.screen = screen
        self.NoiceSpeed()

    def Die(self):
        self.rect.x = 1000
        self.barrier.rect.x = self.rect.x
        self.barrier.rect.y = self.rect.y
        self.barrier.image = load_image(choice(self.barrier.type))
        self.barrier.image = pygame.transform.scale(self.barrier.image, (42, 42))
        self.barrier.pls = False
        self.barrier.endY = 296

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.rect.x <= 1000 and self.count_box == 1:
            self.count_box = 0
            self.barrier = Barrier(self.rect.x - 10, 150, ['Icons/Barrel1.png', 'Icons/Barrel2.png', 'Icons/Barrel3.png',
                                                      'Icons/Box1.png', 'Icons/Box2.png', 'Icons/Box3.png',
                                                      'Icons/Box4.png', 'Icons/Box5.png',
                                                      'Icons/Box6.png', 'Icons/Box8.png',
                                                      'Icons/Pointer1.png', 'Icons/Pointer2.png'], self.screen, self.selected_option)

        if self.barrier:
            self.barrier.draw()
            self.barrier.Moving()

        if self.barrier.rect.x <= self.barrier.DiedX:
            self.barrier.rect.x = self.rect.x
            self.barrier.rect.y = self.rect.y
            self.barrier.image = load_image(choice(self.barrier.type))
            self.barrier.image = pygame.transform.scale(self.barrier.image, (42, 42))
            self.barrier.Vect = 0.5
            self.barrier.pls = False

        if self.rect.x < self.DiedX:
            self.Die()
            self.count_box = 1

        if self.barrier.delete:
            self.barrier.image = load_image('Icons/plus.png')
            self.barrier.image = pygame.transform.scale(self.barrier.image, (42, 42))
            self.barrier.delete = False
            self.barrier.pls = True


class Barrier(Mov, pygame.sprite.Sprite):
    def __init__(self, x, y, tp, screen, sel):
        super().__init__()
        self.x, self.y = x, y
        self.endY = 296
        self.type = tp
        self.DiedX = -200
        self.delete = False
        self.pls = False
        self.image = load_image(choice(self.type))
        self.image = pygame.transform.scale(self.image, (42, 42))
        self.count = 0
        self.Vect = 0.5
        self.rect = Rect(self.x, self.y, 42, 42)
        self.selected_option = sel
        self.screen = screen
        self.NoiceSpeed()

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.count += 1


class Enemy(Mov, pygame.sprite.Sprite):
    def __init__(self, screen, sel, icon, bulIcon):
        super().__init__()
        self.Time = 0
        self.hp = 1
        self.DiedX = -200
        self.image = load_image(icon)#'Icons/enemy.png')
        self.image = pygame.transform.scale(self.image, (42, 64))
        self.mask = pygame.mask.from_surface(self.image)
        self.x = randint(1000, 2000)
        self.y = 273
        self.bul = Bullet('lazer', self.x, self.y + 25, screen, sel)
        self.bul.isAlive = False
        self.rect = Rect(self.x, self.y, 42, 64)
        self.selected_option = sel
        self.screen = screen
        self.NoiceSpeed()

    def Die(self):
        self.rect.x = randint(1000, 2000)

    def draw(self):
        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.bul.draw()
        self.bul.Moving()
        if self.bul.collide:
            self.bul.rect.x = self.rect.x
            self.bul.collide = False

    def Moving(self):
        self.rect.x -= self.speed
        if self.rect.x <= self.DiedX:
            self.Die()

        self.Time += 1

        if self.Time >= 1000:
            self.Time = 0

    def Fire(self):
        self.bul = Bullet('lazer', self.x, self.y + 30, self.screen, self.selected_option)
        self.Time = 0

        if self.bul.x <= bul.DiedX:
            self.bul.Die()
            self.bul.x = self.x
            self.bul.y = self.y