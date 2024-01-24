import os
import sys
from operator import itemgetter
from random import randint, choice
import pygame
from pygame import *
import sqlite3
from Architecture import *
from BadMan import *
from Player import *
from Wind import *
from Glob import *

vol = 0.5
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()
pygame.mixer.music.load(choice(musikDisk))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(vol)
pygame.mixer.music.pause()

clickSound = pygame.mixer.Sound('Sounds/Click.mp3')


def draw_selector():
    FNT = pygame.font.Font(None, 36)
    for indx, option in enumerate(options):
        Rct = pygame.Rect(50, 50 + indx * 50, 290, 40)
        pygame.draw.rect(screen, WHITE, Rct)
        pygame.draw.rect(screen, BLACK, Rct, 2)
        text = FNT.render(option, True, BLACK)
        text_rect = text.get_rect(center=Rct.center)
        screen.blit(text, text_rect)


def draw_text(wind, text, x, y):
    FNT = pygame.font.Font(None, 50)
    text_surface = FNT.render(text, True, (255, 0, 0))
    wind.blit(text_surface, (x, y))


flagRes = False
pygame.init()
pygame.display.set_caption('Moon Escape')
clock = pygame.time.Clock()
FPS = 60
running = True
PlayerAnimCount = 0
is_Jump = False
Jump_count = 10

input_rect = pygame.Rect(200, 200, 140, 32)
color_active = pygame.Color('lightskyblue3')
color_passive = pygame.Color('chartreuse4')
color = color_passive
active = False

size = width, height = 1000, 400
screen = pygame.display.set_mode(size)
isPlayClick = False
isPlay = False
isBestScoreTable = False
pause = False
reset = False
EndGame = False

DB_NAME = 'TextFiles/bestScoreTable.sqlite'
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
bg1 = None
bg2 = None
bg3 = None
bb1 = None
bb2 = None
bb3 = None
all_Die_sprites = [enemy, enemy]

while running:
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

    if selected_option is not None and flagRes or reset:
        bg1 = Background(0, 0, screen, selected_option)
        bg2 = Background(1000, 0, screen, selected_option)
        bg3 = Background(2000, 0, screen, selected_option)
        bb1 = BB(0, 63, selected_option, screen)
        bb2 = BB(1000, 63, selected_option, screen)
        bb3 = BB(2000, 63, selected_option, screen)
        Turba = Truba(screen, selected_option)
        person = Person(screen)
        enemy = Enemy(screen, selected_option)
        door = Door(screen, selected_option)
        all_Die_sprites = [enemy, Enemy(screen, selected_option)]
        platformss = [Platforms(screen, selected_option)]
        flagRes = False
        reset = False
        Jump_count = 10
        Fall_count = 0
        is_is_PlatformCollide = False
        score = 0
        money = 0
        all_money = [Money(screen, selected_option)]

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
                    platformss.append(Platforms(screen, selected_option))

            for i in all_money:
                i.draw()

            for i in all_money:
                i.Moving()
                if i.x <= -2400 or i.Collid:
                    del all_money[all_money.index(i)]
                    break
                if i.step == 30:
                    all_money.append(Money(screen, selected_option))
                if pygame.sprite.collide_mask(i, person):
                    money += 1
                    i.Collid = True

            for i in all_Die_sprites:
                if i:
                    i.draw()
                    i.Moving()
                    if person.rect.y == i.rect.y and i.Time >= 1000:
                        i.Fire()
                    if pygame.sprite.collide_mask(i, person):
                        i.Die()
                if pygame.sprite.collide_mask(i.bul, person):
                    i.bul.collide = True
                    i.bul.Die()
                    person.rect.x -= 100

            Turba.draw()
            Turba.Moving()

            if pygame.sprite.collide_mask(Turba.barrier, person):
                if not Turba.barrier.pls:
                    person.rect.x -= 100
                    Turba.barrier.rect.x = Turba.rect.x
                    Turba.barrier.rect.y = Turba.rect.y
                else:
                    if person.rect.x < 400:
                        person.rect.x += 100
                Turba.barrier.rect.x = 3000
                Turba.barrier.rect.y = -1000
                Turba.barrier.image = load_image(choice(Turba.barrier.type))
                Turba.barrier.image = pygame.transform.scale(Turba.barrier.image, (42, 42))
                Turba.barrier.Vect = 0.5
                Turba.barrier.pls = False

            for i in platformss:
                if Turba.barrier.rect.y < Turba.barrier.endY and not pygame.sprite.collide_mask(Turba.barrier, i):
                    Turba.barrier.rect.y += Turba.barrier.Vect
                else:
                    Turba.barrier.delete = True
                    Turba.barrier.Vect = 0

            person.draw()

            door.draw()

            if pygame.sprite.collide_mask(door.MasterCard, person):
                door.MasterCard.Collid = True
                door.MasterCard.DieFlag = True
            if pygame.sprite.collide_mask(door, person) and door.AnimCount < 40:
                person.rect.x -= 100
                door.Die()

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