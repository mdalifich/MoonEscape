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


class Mov(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.DiedX = -200
        self.speed = 10

    def Die(self):
        pass

    def Moving(self):
        self.x -= self.speed
        if self.x <= self.DiedX:
            self.Die()


class Barrier(Mov, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.DiedX = -200
        self.image = load_image('Icons/ExitIcon.png', (255, 255, 255))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def Die(self):
        global barrier
        barrier = None


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


class Bullet(Mov, pygame.sprite.Sprite):
    def __init__(self, typebul, x, y):
        super().__init__()
        self.coef = -1
        self.image = load_image(f'Icons/{typebul}.png', (255, 255, 255))
        self.typeBullet = typebul
        self.isAlive = True
        self.DiedX = -200
        self.x, self.y = x, y
        if self.typeBullet == 'Arrow':
            self.speed = 20

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def Die(self, x, y):
        self.x, self.y = x, y
        self.coef = -1

    def Moving(self):
        self.x -= self.speed
        self.y += self.coef
        if self.y <= 575:
            self.coef = 1


class Enemy(Mov, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = 1
        self.x, self.y = 350, 600
        self.DiedX = -200
        self.image = load_image('Icons/person1.png', (255, 255, 255))

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def Die(self):
        global enemy
        enemy = None

    def Moving(self):
        self.x -= self.speed
        if self.x <= self.DiedX:
            # self.Die()
            self.x = 1920
        if self.y - person.y == 0:
            self.Fire()


    def Fire(self):
        global bul
        if not bul.isAlive:
            bul = Bullet('Arrow', self.x, self.y + 25)
            bul.draw()
        if bul.x <= bul.DiedX:
            bul.Die(self.x, self.y + 25)




if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Пам парам')
    size = width, height = 1920, 768
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    person = Person()
    FPS = 60
    barrier = Barrier(1920, 600)
    enemy = Enemy()
    bul = Bullet('Arrow', -10, 550)
    running = True
    fall = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                person.jump()
            if True in key and key[pygame.K_SPACE]:
                fall = False
            else:
                fall = True

        screen.fill((255, 255, 255))
        if barrier is not None:
            barrier.draw()
            barrier.Moving()

        if fall:
            if person.y < 600:
                person.fall()

        if enemy is not None:
            enemy.draw()
            enemy.Moving()
            bul.draw()
            bul.Moving()
            if enemy.x == person.x and person.y >= 550:
                enemy.Die()

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