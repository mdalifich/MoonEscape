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
        self.image = load_image('Icons/ExitIcon.png', (255, 255, 255))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def Die(self):
        self.close()

    def Moving(self):
        self.x -= 10
        if self.x <= self.DiedX:
            #self.Die()
            self.x = 1024


class Person(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = 5
        self.weapon = 0
        self.image = load_image('Icons/person1.png', (255, 255, 255))
        self.x, self.y = 350, 600

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def jump(self):
        if self.y == 600:
            self.y -= 200
        elif self.y >= 20:
            self.y -= 10

    def fall(self):
        self.y += 10


class Bullet(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.image = load_image('Icons/person1.png', (255, 255, 255))
        self.typeBullet = type
        self.isAlife = True
        if self.typeBullet == 'Arrow':
            self.speed = 20

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def Die(self):
        self.close()

    def Moving(self):
        self.x -= self.speed
        if self.x <= self.DiedX:
            self.isAlife = False
            self.Die()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = 1
        self.image = load_image('Icons/person1.png', (255, 255, 255))
        self.isFire = False
        self.x, self.y = 350, 600

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def Die(self):
        self.close()

    def Moving(self):
        self.x -= 10
        if self.x <= self.DiedX:
            # self.Die()
            self.x = 1024
        if self.y - person.y <= 100:
            if not isFire:
                self.Fire()

    def Fire(self):
        self.bullet = Bullet('Arrow')
        self.bullet.draw()
        self.bullet.Moving()
        self.isFire = self.isAlive


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
    enemy = Enemy()
    running = True
    fall = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                person.jump()
            if True in key:
                fall = False
            else:
                fall = True

        screen.fill((255, 255, 255))
        barrier.draw()
        barrier.Moving()
        if fall:
            if person.y < 600:
                person.fall()

        enemy.draw()
        enemy.Moving()
        person.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
s = '''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Menu()
    ex.show()
    sys.exit(app.exec())'''