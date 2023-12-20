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


class Barrier(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.DiedX = -200
        self.image = load_image('person1.png', (255, 255, 255))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def Die(self):
        self.close()

    def Moving(self):
        self.x -= 1


class Person(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = 5
        self.weapon = 0
        self.is_jump = True
        self.is_fly = False
        self.image = load_image('person1.png', (255, 255, 255))
        self.x, self.y = 350, 600

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


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
    clock = pygame.time.Clock()
    person = Person()
    FPS = 60
    barrier = Barrier(1024, 600)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        barrier.draw()
        barrier.Moving()
        person.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec())
