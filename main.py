import os
import pygame
import sys

score = 0

def draw_text(screen, text, x, y):
    font = pygame.font.Font(None, 50)
    text_surface = font.render(text, True, (255, 0, 0))
    screen.blit(text_surface, (x, y))

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
        self.animList = ['Icons/person1.png', 'Icons/person2.png', 'Icons/person3.png', 'Icons/person4.png',
                         'Icons/person5.png']
        self.hp = 5
        self.weapon = 0
        self.image = load_image(self.animList[0])
        self.image = pygame.transform.scale(self.image, (45, 77))
        self.rect = self.image.get_rect(center=(300, 300))
        self.mask = pygame.mask.from_surface(self.image)

    def AnimationUpdate(self, i):
        self.image = load_image(self.animList[i])
        self.image = pygame.transform.scale(self.image, (45, 77))


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
        self.coef = -1
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
        self.coef = -1

    def Moving(self):
        self.x -= self.speed
        self.y += self.coef
        if self.y <= 275:
            self.coef = 1


class Enemy(Mov, pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.hp = 1
        self.DiedX = -200
        self.image = load_image('Icons/person1.png')
        self.image = pygame.transform.scale(self.image, (45, 77))
        self.rect = self.image.get_rect(center=(1000, 300))

    def Die(self):
        enemy.kill()

    def update(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        self.rect.x -= self.speed
        if self.rect.x <= -200:
            self.Die()
        if pygame.sprite.collide_mask(self, person):
            self.Die()
            person.rect.x -= 100

    def Fire(self):
        global bul
        if not bul.isAlive:
            bul = Bullet('Arrow', self.x, self.y + 25)
            bul.draw()
        if bul.x <= bul.DiedX:
            bul.Die()
            bul.x = self.x
            bul.y = self.y


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Пам парам')
    size = width, height = 1000, 400
    screen = pygame.display.set_mode(size)

    all_sprites = pygame.sprite.Group()
    clock = pygame.time.Clock()
    person = Person()
    FPS = 60
    barrier = Barrier(1000, 300)
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
            if Jump_count >= -10:
                if Jump_count < 0:
                    person.rect.y += (Jump_count ** 2) / 2
                else:
                    person.rect.y -= (Jump_count ** 2) / 2
                Jump_count -= 1
            else:
                is_Jump = False
                Jump_count = 10
        if person.rect.y >= 262:
            person.rect.y = 262

        screen.fill((255, 255, 255))
        if barrier is not None:
            barrier.draw()
            barrier.Moving()


        draw_text(screen, f"Очки: {score}", 5, 10)

        if all_sprites:
            all_sprites.update()
        else:
            enemy = Enemy()
            all_sprites.add(enemy)
        if PlayerAnimCount > 40:
            score += 1
            PlayerAnimCount = 0
        if PlayerAnimCount % 10 == 0:
            person.AnimationUpdate(PlayerAnimCount // 10)
        PlayerAnimCount += 1
        person.draw()
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
