import os
import pygame
from random import randint, choice


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
        print(selected_option)
        if selected_option == 'Легкая сложность':
            self.speed = 10
        elif selected_option == 'Нормальная сложность':
            self.speed = 20
        elif selected_option == 'Сложная сложность':
            self.speed = 30
        elif selected_option == 'Non real':
            self.speed = 40
        self.step = 0

    def Die(self):
        pass

    def Moving(self):
        self.x -= self.speed
        if self.x <= self.DiedX:
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
        self.rect = self.image.get_rect(center=(1000, 50))
        self.count_box = 1

    def Die(self):
        self.rect.x = randint(1000, 2000)

    def update(self):
        global barrier
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.rect.x -= self.speed
        if self.rect.x <= 1000 and self.count_box == 1:
            self.count_box = 0
            barrier = Barrier(self.rect.x - 10, 150, ['Icons/Box1.png'])


        if self.rect.x < self.DiedX:
            self.Die()
            self.count_box = 1
            if barrier:
                barrier = None




class Barrier(Animated, Mov, pygame.sprite.Sprite):
    def __init__(self, x, y, tp):
        super().__init__()
        self.x, self.y = x, y
        self.type = tp
        self.DiedX = -200
        self.image = load_image(self.type[0])
        self.rect = self.image.get_rect(center=(1000, 305))
        self.count = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y - 63))
        if self.y < 343:
            global platformss
            for i in platformss:
                if not pygame.sprite.collide_mask(self, i):
                    self.y += self.speed
        if self.count > len(self.animList) * 10:
            self.count = 0
        if self.count % 10 == 0:
            self.AnimationUpdate(self.count // 10 - 1)
        self.count += 1

    def Die(self):
        self.x = randint(1000, 2000)


class Person(Animated, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animList = ['Icons/person1.png', 'Icons/person2.png', 'Icons/person3.png', 'Icons/person4.png',
                         'Icons/person5.png']
        self.hp = 5
        self.weapon = 0
        self.image = load_image(self.animList[0])
        self.image = pygame.transform.scale(self.image, (42, 64))
        self.rect = self.image.get_rect(center=(300, 305))
        self.mask = pygame.mask.from_surface(self.image)
        self.scale = (42, 64)

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

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def Die(self):
        self.coef = -6
        self.x = enemy.rect.x
        self.y = enemy.rect.y + 20

    def Moving(self):
        self.x -= self.speed + 10
        self.y += self.coef
        self.coef += 0.25
        if self.x <= self.DiedX:
            self.Die()


class Enemy(Mov, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = 1
        self.DiedX = -200
        self.image = load_image('Icons/enemy.png')
        self.image = pygame.transform.scale(self.image, (42, 64))
        self.rect = self.image.get_rect(center=(1000, 305))

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
            person.rect.x -= 100
        if person.rect.y == self.rect.y:
            self.Fire()

    def Fire(self):
        global bul
        if not bul.isAlive:
            bul = Bullet('Arrow', self.x, self.y + 25)
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

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def Die(self):
        self.x = 2000


class BB(Mov, pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x, self.y = x, y
        self.speed = 1
        self.DiedX = -1000
        self.image = load_image('Icons/BBackground.png')

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def Die(self):
        self.x = 2000

    def Moving(self):
        self.x -= self.speed
        if self.x <= self.DiedX:
            self.Die()


class Platforms(Mov, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.DiedX = -130
        self.image = load_image('Icons/platform.png')
        self.rect = self.image.get_rect()
        self.y = randint(150, 250)
        self.x = 1000

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

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
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

screen = None
platformss = None
person = None
barrier = None
enemy = None
bul = None
truba = None
score = 0
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

options = ['Легкая сложность', 'Нормальная сложность', 'Сложная сложность', 'Non real']
selected_option = None

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
    global score, screen, enemy, barrier, bul, platformss, WHITE, BLACK, selected_option, person, truba, bg1, bg2, bg3, bb1, bb2, bb3
    flag = True
    pygame.init()
    pygame.display.set_caption('Moon Escape')
    clock = pygame.time.Clock()
    FPS = 60
    running = True
    fall = False
    PlayerAnimCount = 0
    is_Jump = False
    Jump_count = 10

    size = width, height = 1000, 400
    screen = pygame.display.set_mode(size)
    isPlayClick = False
    isPlay = False
    isBestScoreTable = False
    pause = False
    reset = False

    while running:
        if not isPlay and not isPlayClick:
            screen.fill(BLACK)

        # Создание кнопок и рисование
        play_button = Button('Играть', 400, 100, 200, 50, (0, 255, 0))
        leader_button = Button('Таблица лидеров', 400, 200, 200, 50, (0, 255, 0))
        exit_button = Button('Выход', 400, 300, 200, 50, (0, 255, 0))
        RemakeBTN = Button('Назад', 50, 350, 200, 50, (0, 255, 0))
        OkBTN = Button('Готово', 400, 50, 200, 50, (0, 255, 0))
        LevelDanger = Button('', 400, 200, 200, 50, (0, 255, 0))

        if not isPlayClick and not isBestScoreTable and not isPlay:
            play_button.draw(screen, WHITE)
            leader_button.draw(screen, WHITE)
            exit_button.draw(screen, WHITE)
        else:
            RemakeBTN.draw(screen, WHITE)

        if isPlayClick:
            OkBTN.draw(screen, WHITE)
            LevelDanger.draw(screen, WHITE)

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
                if not isPlay:
                    for i in range(len(options)):
                        rect = pygame.Rect(50, 50 + i * 50, 200, 40)
                        if rect.collidepoint(event.pos):
                            selected_option = options[i]
                            reset = True
                    # Проверка нажатия кнопок
                    if play_button.is_over(pos):
                        isPlayClick = True
                    if leader_button.is_over(pos):
                        isBestScoreTable = True
                    if exit_button.is_over(pos):
                        running = False
                    if OkBTN.is_over(pos):
                        if selected_option is not None:
                            isPlay = True
                            isPlayClick = False

                if RemakeBTN.is_over(pos):
                    isBestScoreTable = False
                    isPlayClick = False
                    isPlay = False

        if selected_option is not None and flag or reset:
            bg1 = Background(0, 0)
            bg2 = Background(1000, 0)
            bg3 = Background(2000, 0)
            bb1 = BB(0, 63)
            bb2 = BB(1000, 63)
            bb3 = BB(2000, 63)
            truba = Truba()
            person = Person()
            enemy = Enemy()
            bul = Bullet('Arrow', -10, 250)
            platformss = [Platforms()]
            flag = False
            reset = False

        if isPlayClick:
            screen.fill(WHITE)
            draw_selector()

        if isBestScoreTable:
            pass

        if isPlay and not pause:
            if is_Jump:
                person.image = load_image('Icons/personJump.png')
                person.image = pygame.transform.scale(person.image, (50, 64))
                if Jump_count >= -10:
                    if Jump_count < 0:
                        person.rect.y += (Jump_count ** 2) / 2
                    else:
                        person.rect.y -= (Jump_count ** 2) / 2
                    Jump_count -= 1
                else:
                    is_Jump = False
                    Jump_count = 10
            else:
                if PlayerAnimCount > 40:
                    score += 1
                    PlayerAnimCount = 0
                if PlayerAnimCount % 10 == 0:
                    person.AnimationUpdate(PlayerAnimCount // 10)
                PlayerAnimCount += 1

            if person.rect.y >= 273:
                person.rect.y = 273


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
            bb3.Moving()##

            for i in platformss:
                i.draw()

            for i in platformss:
                i.Moving()
                if i.x <= i.DiedX:
                    del platformss[platformss.index(i)]
                    break
                if i.step == 30:
                    platformss.append(Platforms())
                if pygame.sprite.collide_mask(i, person):
                    is_Jump = False

            if barrier != None:
                barrier.draw()
                barrier.Moving()

            truba.update()

            bul.draw()
            bul.Moving()

            draw_text(screen, f"Очки: {score}", 5, 10)

            enemy.draw()
            enemy.Moving()

            person.draw()

            if not isPlayClick and not isBestScoreTable and not isPlay:
                play_button.draw(screen, WHITE)
                leader_button.draw(screen, WHITE)
                exit_button.draw(screen, WHITE)
            else:
                RemakeBTN.draw(screen, WHITE)

            pygame.display.flip()
            clock.tick(FPS)
    pygame.quit()

game()
