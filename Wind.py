import os
import sys
from operator import itemgetter
from random import randint, choice
import pygame
from pygame import *
from MatClasses import *
from Glob import *


class Button:
    def __init__(self, text, x, y, width, height, color):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self, scrn, outline=None):
        if outline:
            pygame.draw.rect(scrn, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
        pygame.draw.rect(scrn, self.color, (self.x, self.y, self.width, self.height), 0)

        font = pygame.font.SysFont(None, 30)
        text = font.render(self.text, 1, (255, 255, 25))
        scrn.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False