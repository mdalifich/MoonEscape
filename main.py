import os
import sys
from operator import itemgetter
from random import randint, choice
import pygame
from pygame import *
import sqlite3


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
        global selected_option
        self.x = 0
        self.y = 0
        self.DiedX = -200
        self.rect = Rect(0, 0, 1, 1)
        if selected_option == 'Легкая сложность':
            self.speed = 5
        elif selected_option == 'Нормальная сложность':
            self.speed = 10
        elif selected_option == 'Сложная сложность':
            self.speed = 15
        elif selected_option == 'Non real':
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


class Truba(Mov, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_image('Icons/Turba.png')
        self.image = pygame.transform.scale(self.image, (32, 96))
        self.rect = Rect(1000, 0, 32, 96)
        self.count_box = 1

    def Die(self):
        self.rect.x = 1000
        global barrier
        barrier.rect.x = self.rect.x
        barrier.rect.y = self.rect.y
        barrier.image = load_image(choice(barrier.type))
        barrier.image = pygame.transform.scale(barrier.image, (42, 42))
        barrier.pls = False
        barrier.endY = 296

    def draw(self):
        global barrier
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if self.rect.x <= 1000 and self.count_box == 1:
            self.count_box = 0
            barrier = Barrier(self.rect.x - 10, 150, ['Icons/Barrel1.png', 'Icons/Barrel2.png', 'Icons/Barrel3.png',
                                                      'Icons/Box1.png', 'Icons/Box2.png', 'Icons/Box3.png',
                                                      'Icons/Box4.png', 'Icons/Box5.png',
                                                      'Icons/Box6.png', 'Icons/Box8.png',
                                                      'Icons/Pointer1.png', 'Icons/Pointer2.png'])

        if barrier:
            barrier.draw()
            barrier.Moving()

        if barrier.rect.x <= barrier.DiedX:
            barrier.rect.x = self.rect.x
            barrier.rect.y = self.rect.y
            barrier.image = load_image(choice(barrier.type))
            barrier.image = pygame.transform.scale(barrier.image, (42, 42))
            barrier.Vect = 0.5
            barrier.pls = False

        if pygame.sprite.collide_mask(barrier, person):
            global collis
            collis = True
            if not barrier.pls:
                person.rect.x -= 100
                barrier.rect.x = self.rect.x
                barrier.rect.y = self.rect.y

            barrier.image = load_image(choice(barrier.type))
            barrier.image = pygame.transform.scale(barrier.image, (42, 42))
            barrier.Vect = 0.5
            barrier.pls = False
        if self.rect.x < self.DiedX:
            self.Die()
            self.count_box = 1


class Barrier(Mov, pygame.sprite.Sprite):
    def __init__(self, x, y, tp):
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

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

        for i in platformss:
            if self.rect.y < self.endY and not pygame.sprite.collide_mask(self, i):
                self.rect.y += self.Vect
            else:
                self.delete = True
                self.Vect = 0
        self.count += 1

        if self.delete:
            barrier.image = load_image('Icons/plus.png')
            barrier.image = pygame.transform.scale(self.image, (42, 42))
            barrier.delete = False
            barrier.pls = True

        if pygame.sprite.collide_mask(self, person) and self.pls:
            if person.rect.x < 400:
                person.rect.x += 100
            self.rect.x = 3000
            self.rect.y = -1000
            self.Vect = 0.5
            barrier.pls = False


class Person(Animated, pygame.sprite.Sprite):
    def __init__(self):
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

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def jump(self):
        if self.rect.y == 300:
            self.rect.y -= 200
        elif self.rect.y >= 20:
            self.rect.y -= 10

    def fall(self):
        self.rect.y += 10


class Bullet(Mov, pygame.sprite.Sprite):
    def __init__(self, typebul, x, y):
        super().__init__()
        self.coef = -6
        self.image = load_image(f'Icons/{typebul}.png')
        self.image = pygame.transform.scale(self.image, (30, 8))
        self.typeBullet = typebul
        self.isAlive = True
        self.DiedX = -1000
        self.x, self.y = x, y
        self.rect = Rect(self.x, self.y, 30, 8)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def Die(self):
        self.coef = -6
        self.rect.x = enemy.rect.x
        self.rect.y = enemy.rect.y + 20
        lazerSound.play()
        print('lazer')

    def Moving(self):
        self.rect.x -= self.speed + 10
        if self.typeBullet == 'Arrow':
            self.rect.y += self.coef
        self.coef += 0.25
        if self.rect.x <= self.DiedX:
            self.Die()
        if pygame.sprite.collide_mask(self, person):
            global collis
            collis = True
            self.Die()
            person.rect.x -= 100


class Enemy(Mov, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = 1
        self.DiedX = -200
        self.image = load_image('Icons/enemy.png')
        self.image = pygame.transform.scale(self.image, (42, 64))
        self.mask = pygame.mask.from_surface(self.image)
        self.x = 1000
        self.y = 273
        self.rect = Rect(self.x, self.y, 42, 64)

    def Die(self):
        self.rect.x = randint(1000, 2000)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def Moving(self):
        self.rect.x -= self.speed
        if self.rect.x <= self.DiedX:
            self.Die()
        if pygame.sprite.collide_mask(self, person):
            self.Die()
            global collis
            collis = True
        if person.rect.y == self.rect.y:
            self.Fire()

    def Fire(self):
        global bul
        if not bul.isAlive:
            bul = Bullet('lazer', self.x, self.y + 25)
            bul.draw()
        if bul.x <= bul.DiedX:
            bul.Die()
            bul.x = self.x
            bul.y = self.y


class Background(Mov, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.DiedX = -1000
        self.image = load_image('Icons/BackGround.png')
        self.rect = Rect(self.x, self.y, 1000, 400)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def Die(self):
        self.rect.x = 2000


class BB(Mov, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.speed = 1
        self.DiedX = -1000
        self.iconList = {'Легкая сложность': 'Icons/BBackground.png', 'Нормальная сложность': 'Icons/fon2.png',
                         'Сложная сложность': 'Icons/fon3.png', 'Non real': 'Icons/Fon1.png'}
        global selected_option
        self.image = load_image(self.iconList[selected_option])
        self.rect = Rect(self.x, self.y, 1000, 274)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def Die(self):
        self.rect.x = 2000

    def Moving(self):
        self.rect.x -= self.speed
        if self.rect.x <= self.DiedX:
            self.Die()


class Platforms(Mov, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.DiedX = -2405
        self.image = load_image('Icons/platform.png').convert_alpha()
        self.n = randint(15, 80)
        self.mask = pygame.mask.from_surface(self.image)
        self.y = randint(150, 250)
        self.x = 1000
        self.rect = Rect(self.x, self.y, 96, 32)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def Die(self):
        self.kill()


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


class Money(Animated, Mov, pygame.sprite.Sprite):
    def __init__(self):
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

    def Die(self):
        self.kill()

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if pygame.sprite.collide_mask(self, person):
            global money
            money += 1
            self.Collid = True
            self.Die()
        self.AnimCount += 1
        if self.AnimCount > 50:
            self.AnimCount = 0
        if self.AnimCount % 10 == 0:
            self.AnimationUpdate(self.AnimCount // 10)


class Card(Animated, Mov, pygame.sprite.Sprite):
    def __init__(self):
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

    def Die(self):
        global OpenTheDoors, door
        if not OpenTheDoors or door.die:
            self.rect.x = door.rect.x - 250
            door.die = False
        self.y = randint(150, 280)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        if pygame.sprite.collide_mask(self, person):
            global OpenTheDoors
            OpenTheDoors = True
            self.Collid = True
            self.Die()
        self.AnimCount += 1
        if self.AnimCount > 70:
            self.AnimCount = 0
        if self.AnimCount % 10 == 0:
            self.AnimationUpdate(self.AnimCount // 10)


class Door(Animated, Mov, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
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
        self.MasterCard = Card()

    def Die(self):
        self.rect.x = randint(2500, 4000)
        self.AnimCount = 0
        self.image = load_image(self.animList[0])
        self.image = pygame.transform.scale(self.image, (128, 274))
        self.MasterCard.Collid = False
        global OpenTheDoors
        OpenTheDoors = False
        self.die = True

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.MasterCard.draw()
        self.MasterCard.Moving()
        if pygame.sprite.collide_mask(self, person) and self.AnimCount < 40:
            person.rect.x -= 100
            self.Die()
        if self.MasterCard.Collid:
            if self.AnimCount < 40:
                self.AnimCount += 1
            if self.AnimCount % 10 == 0:
                self.AnimationUpdate(self.AnimCount // 10)
                self.image = pygame.transform.scale(self.image, (128, 274))

DB_NAME = 'moon_escape.sqlite'
screen = None
platformss = None
all_money = None
person = None
barrier = None
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
vol = 0.5
flag_game_over = 0

pygame.mixer.pre_init(44100, -16, 1, 512)

pygame.mixer.init()
pygame.mixer.music.load(choice(musikDisk))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(vol)
pygame.mixer.music.pause()

lazerSound = pygame.mixer.Sound('Sounds/Lazer.mp3')
clickSound = pygame.mixer.Sound('Sounds/Click.mp3')

options = ['Легкая сложность', 'Нормальная сложность', 'Сложная сложность', 'Non real']
selected_option = None
collis = False

# создание функции для отображения селектора
def draw_selector():
    font = pygame.font.Font(None, 36)
    for i, option in enumerate(options):
        rect = pygame.Rect(50, 50 + i * 50, 290, 40)
        pygame.draw.rect(screen, WHITE, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        text = font.render(option, True, BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)


def game():
    global score, screen, enemy, barrier, bul, platformss, WHITE, BLACK, selected_option, person, collis, \
        Turba, is_is_PlatformCollide, Fall_count, money, all_money, name, door, vol, flag_game_over
    flag = True
    pygame.init()
    pygame.display.set_caption('Moon Escape')
    clock = pygame.time.Clock()
    FPS = 60
    running = True
    PlayerAnimCount = 0
    is_Jump = False
    Jump_count = 10

    flag_game_over = 0

    input_rect = pygame.Rect(200, 200, 140, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    active = False

    sqlite = sqlite3.connect(DB_NAME)

    size = width, height = 1000, 400
    screen = pygame.display.set_mode(size)
    isPlayClick = False
    isPlay = False
    isBestScoreTable = False
    pause = False
    reset = False
    all_Die_sprites = []
    bg1 = None
    bg2 = None
    bg3 = None
    bb1 = None
    bb2 = None
    bb3 = None
    EndGame = False

    while running:
        print('Цикл')
        if not isPlay and not isPlayClick:
            screen.fill(BLACK)

        # Создание кнопок и рисование

        play_button = Button('Играть', 400, 100, 200, 50, (0, 255, 0))
        leader_button = Button('Таблица лидеров', 400, 200, 200, 50, (0, 255, 0))
        exit_button = Button('Выход', 400, 300, 200, 50, (0, 255, 0))
        OkBTN = Button('Готово', 400, 50, 200, 50, (0, 255, 0))
        BackBtn = Button('Назад', 50, 350, 200, 50, (0, 255, 0))
        RemakeBTN = Button('Начать заного', 50, 100, 200, 50, (0, 255, 0))

        if isPlayClick:
            screen.fill(BLACK)
            draw_selector()

        if isBestScoreTable:
            cur = sqlite.cursor()
            cur.execute('SELECT * FROM result')
            sp = cur.fetchall()
            draw_text(screen, 'Топ 5', 440, 20)
            k = 1
            sp_right = sorted(sp, key=itemgetter(2), reverse=True)
            for i in range(len(sp_right)):
                draw_text(screen, f'{k}.{sp_right[i][1]} — Количество очков {sp_right[i][2]}', 200, 40 + k * 35)
                k += 1
                if k > 5:
                    break

        if not isPlayClick and not isBestScoreTable and not isPlay:
            play_button.draw(screen, WHITE)
            leader_button.draw(screen, WHITE)
            exit_button.draw(screen, WHITE)
            draw_text(screen, f'Введите свой ник:', 350, 10)
            draw_text(screen, name, 450, 45)
        else:
            BackBtn.draw(screen, WHITE)

        if isPlayClick:
            OkBTN.draw(screen, WHITE)
            global selected_option
            if selected_option is not None:
                draw_text(screen, selected_option, 400, 200)

        pygame.display.update()

        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                running = False

            key = pygame.key.get_pressed()

            if key[pygame.K_SPACE]:
                is_Jump = True

            if key[pygame.K_ESCAPE]:
                pause = not pause

            if event.type == pygame.MOUSEBUTTONDOWN:

                if RemakeBTN.is_over(pos) and EndGame:
                    reset = True
                if not isPlay:
                    for i in range(len(options)):
                        rect = pygame.Rect(50, 50 + i * 50, 200, 40)
                        if rect.collidepoint(event.pos):
                            selected_option = options[i]
                            reset = True
                    # Проверка нажатия кнопок
                    if not isPlay and not isPlayClick:
                        if play_button.is_over(pos) and name != '':
                            clickSound.play()
                            isPlayClick = True
                        if leader_button.is_over(pos):
                            clickSound.play()
                            isBestScoreTable = True
                        if exit_button.is_over(pos):
                            clickSound.play()
                            running = False
                    if isPlayClick:
                        if OkBTN.is_over(pos):
                            if selected_option is not None:
                                clickSound.play()
                                isPlay = True
                                isPlayClick = False
                if BackBtn.is_over(pos):
                    clickSound.play()
                    isBestScoreTable = False
                    isPlayClick = False
                    isPlay = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_LEFT:
                    vol -= 0.1
                    pygame.mixer.music.set_volume(vol)
                elif event.key == pygame.K_RIGHT:
                    vol += 0.1
                    pygame.mixer.music.set_volume(vol)
                else:
                    if len(name) <= 4:
                        name += event.unicode

            pygame.display.update()

        if selected_option is not None and flag or reset:
            bg1 = Background(0, 0)
            bg2 = Background(1000, 0)
            bg3 = Background(2000, 0)
            bb1 = BB(0, 63)
            bb2 = BB(1000, 63)
            bb3 = BB(2000, 63)
            Turba = Truba()
            person = Person()
            enemy = Enemy()
            door = Door()
            bul = Bullet('lazer', -10, 250)
            all_Die_sprites = [enemy, bul]
            platformss = [Platforms()]
            flag = False
            reset = False
            Jump_count = 10
            Fall_count = 0
            is_is_PlatformCollide = False
            score = 0
            money = 0
            all_money = [Money()]

        if isPlay and not pause and name != '':
            if person.rect.x >= 0:
                EndGame = False
                pygame.mixer.music.unpause()
                is_is_PlatformCollide = False
                for i in platformss:
                    if pygame.sprite.collide_mask(person, i):
                        person.rect.y = i.rect.y - 63
                        is_is_PlatformCollide = True

                if is_Jump:
                    person.image = load_image('Icons/personJump.png')
                    person.image = pygame.transform.scale(person.image, (50, 64))
                    if Jump_count > 0:
                        person.rect.y -= (Jump_count ** 2) / 2
                        Jump_count -= 1
                    else:
                        if Fall_count < 11 and not is_is_PlatformCollide:
                            person.rect.y += (Fall_count ** 2) / 2
                            Fall_count += 1
                        else:
                            Jump_count = 10
                            Fall_count = 0
                            is_Jump = False
                else:
                    Jump_count = 10
                    if PlayerAnimCount > 40:
                        score += 1
                        PlayerAnimCount = 0
                    if PlayerAnimCount % 10 == 0:
                        person.AnimationUpdate(PlayerAnimCount // 10)
                    PlayerAnimCount += 1

                if person.rect.y < 273 and not is_is_PlatformCollide and not is_Jump:
                    person.rect.y += (Fall_count ** 2) / 2
                    Fall_count += 1

                if person.rect.y >= 273:
                    person.rect.y = 273
                    is_Jump = False
                    Fall_count = 0

                bg1.draw()
                bg2.draw()
                bg3.draw()
                bg1.Moving()
                bg2.Moving()
                bg3.Moving()

                bb1.draw()
                bb2.draw()
                bb3.draw()
                bb1.Moving()
                bb2.Moving()
                bb3.Moving()

                for i in platformss:
                    i.draw()

                for i in platformss:
                    i.Moving()
                    if i.x <= -2400:
                        del platformss[platformss.index(i)]
                        break
                    if i.step == i.n + (options.index(selected_option) + 1) * 5:
                        platformss.append(Platforms())

                for i in all_money:
                    i.draw()

                for i in all_money:
                    i.Moving()
                    if i.x <= -2400 or i.Collid:
                        del all_money[all_money.index(i)]
                        break
                    if i.step == 30:
                        all_money.append(Money())

                collis = False
                for i in all_Die_sprites:
                    if i:
                        i.draw()
                        i.Moving()
                if collis:
                    pass

                Turba.draw()
                Turba.Moving()
                person.draw()

                door.draw()
                door.Moving()

                draw_text(screen, f"Метры: {score}", 5, 10)
                draw_text(screen, f"Деньги: {money}", 200, 10)

                if not isPlayClick and not isBestScoreTable and not isPlay:
                    play_button.draw(screen, WHITE)
                    leader_button.draw(screen, WHITE)
                    exit_button.draw(screen, WHITE)
                else:
                    BackBtn.draw(screen, WHITE)

                pygame.display.flip()
                clock.tick(FPS)
            else:
                screen.fill(BLACK)
                draw_text(screen, 'Game Over', 400, 25)
                draw_text(screen, f'Метров пройдено: {score}', 400, 100)
                draw_text(screen, f'Собрано денег: {money}', 400, 150)
                draw_text(screen, f'Бонус за уровень сложности: {options.index(selected_option) * 10}', 400, 200)
                draw_text(screen, f'Итого: {money + score + (options.index(selected_option) * 10)} очков', 400, 325)
                EndGame = True
                flag_game_over += 1
                RemakeBTN.draw(screen, WHITE)
                pygame.mixer.music.pause()
                pygame.mixer.music.rewind()
                if flag_game_over == 1:
                    cur = sqlite.cursor()
                    res = f'INSERT INTO result (name, score) VALUES("{name}", {money + score + (options.index(selected_option) * 10)})'
                    cur.execute(res)
                    sqlite.commit()
                    cur.close()
        else:
            pygame.mixer.music.pause()

    pygame.quit()

game()
