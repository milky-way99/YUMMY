import os
import sys
import pygame

pygame.init()

pygame.mixer.music.load('for_game.mp3')
pygame.mixer.music.play()

size = width, height = 1440, 800
STEP = 5
STEP_BAD = 7
FPS = 50
screen = pygame.display.set_mode(size)
screen.fill((0, 0, 0))

total_pers = "dog.png"
total_food = "bone-3.png"
clock = pygame.time.Clock()
clock2 = pygame.time.Clock()


def load_image(name, color_key=None):
    # функция выгружающая изображения
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


def terminate():
    pygame.quit()
    sys.exit()


c = 0
fon = pygame.transform.scale(load_image('main_background.jpg'), (1440, 800))
screen.blit(fon, (0, 0))

all_sprites = pygame.sprite.Group()


class Chel(pygame.sprite.Sprite):
    chel_image = load_image(total_pers)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Chel.chel_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

pygame.init()
running = True
x, y = 0, 0

while running:
    pygame.mouse.set_visible(True)
    for event in pygame.event.get():
        coords = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
    fon = pygame.transform.scale(load_image('main_background.jpg'), (1440, 800))
    screen.blit(fon, (0, 0))
    all_sprites.draw(screen)
    all_sprites.update()
    pygame.display.flip()
pygame.quit()
