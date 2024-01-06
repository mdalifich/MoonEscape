import os
import pygame
import sys
import pygame_menu
from pygame_menu import themes

pygame.init()
surface = pygame.display.set_mode((600, 400))

def set_difficulty(value, difficulty):
    print(value)
    print(difficulty)

def level_menu():
    mainmenu._open(level)

def start_game():
    pass


mainmenu = pygame_menu.Menu('Welcome', 600, 400, theme=themes.THEME_SOLARIZED)
mainmenu.add.text_input('Name: ', default='Billy Herrington', maxchar=20)
mainmenu.add.button('Играть', level_menu)
mainmenu.add.button('Таблица лидеров')
mainmenu.add.button('Выход', pygame_menu.events.EXIT)

level = pygame_menu.Menu('Выбор сложности', 600, 400, theme=themes.THEME_BLUE)
level.add.selector('Сложность :', [('Лёгкий', 1), ('Средний', 2), ('Сложный', 3), ('Нереальный', 4)], onchange=set_difficulty)
level.add.button('Начать игру', start_game())

mainmenu.mainloop(surface)

score = 0


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


class Animated(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.animList = ['Icons/Box1.png']
        self.image = None
        self.scale = (50, 50)

    def AnimationUpdate(self, i):
        self.image = load_image(self.animList[i])
        self.image = pygame.transform.scale(self.image, self.scale)


class Barrier(Animated, Mov, pygame.sprite.Sprite):
    def __init__(self, x, y, tp):
        super().__init__()
        self.x, self.y = x, y
        self.type = tp
        self.DiedX = -200
        self.image = load_image(self.type[0])
        self.count = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y - 63))
        if self.count > len(self.animList) * 10:
            self.count = 0
        if self.count % 10 == 0:
            self.AnimationUpdate(self.count // 10 - 1)
        self.count += 1

    def Die(self):
        barrier.kill()


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
        self.typeBullet = typebul
        self.isAlive = True
        self.DiedX = -50
        self.x, self.y = x, y
        if self.typeBullet == 'Arrow':
            self.speed = 20

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def Die(self):
        self.coef = -6
        self.x = enemy.rect.x
        self.y = enemy.rect.y + 20

    def Moving(self):
        self.x -= self.speed
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
        #enemy.kill()
        self.rect.x = 1000

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def Moving(self):

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


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Moon Escape')
    size = width, height = 1000, 400
    screen = pygame.display.set_mode(size)

    bg1 = Background(0, 0)
    bg2 = Background(1000, 0)
    bg3 = Background(2000, 0)
    bb1 = BB(0, 63)
    bb2 = BB(1000, 63)
    bb3 = BB(2000, 63)

    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    person = Person()
    FPS = 60
    barrier = Barrier(1000, 300, ['Icons/Box1.png'])
    enemy = Enemy()
    bul = Bullet('Arrow', -10, 250)
    running = True
    fall = False
    PlayerAnimCount = 0
    is_Jump = False
    Jump_count = 10

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE]:
                is_Jump = True

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
        bb3.Moving()

        barrier.draw()
        barrier.Moving()

        bul.draw()
        bul.Moving()

        draw_text(screen, f"Очки: {score}", 5, 10)

        enemy.draw()
        enemy.Moving()

        person.draw()
        
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
