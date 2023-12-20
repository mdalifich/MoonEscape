from PyQt5 import QtGui, QtCore
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
import pygame
import os
import sys


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Windows/MenuWindow.ui', self)


def load_image(name, colorkey=None):
    fullname = os.path.join('', name)
    # если файл не существует, то выходим
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


class Person(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = 5
        self.weapon_cell = 0
        self.is_jump = True
        self.is_fly = False
        self.image = load_image('person1.png', (255, 255, 255))
        self.rect = self.image.get_rect()

    def draw(self):
        screen.blit(self.image, self.rect)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        self.hp = 1


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Пам парам')
    size = width, height = 1024, 768
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()
    person = Person()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        person.draw()
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec())
