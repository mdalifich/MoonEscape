import os
import sys
from operator import itemgetter
from random import randint, choice
import pygame
import sqlite3
from pygame import *

DB_NAME = 'TextFiles/bestScoreTable.sqlite'
screen = None
platformss = None
all_money = None
person = None
enemy = None
bul = None
Turba = None
money = 0
Fall_count = 0
is_is_PlatformCollide = False
score = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
name = ''
OpenTheDoors = False
door = None
musikDisk = ["Sounds/loonboon.mp3", "Sounds/Ken.mp3"]
flag_game_over = 0
options = ['Легкая сложность', 'Нормальная сложность', 'Сложная сложность', 'Non real']
selected_option = None
collis = False
sqlite = sqlite3.connect(DB_NAME)