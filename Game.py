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


def start_screen():
    # запустим начальную заставку игры
    global total_pers, total_food, c
    # create the pygame clock
    intro_text = ["",
                  "Правила игры:",
                  "Перед стартом нажмите либо на кошку либо на собаку в зависсимости от того кем вы хотите управлять",
                  "После нажатия на персонажа, зажмите space",
                  "У вас будет ровно 100 секунд, чтобы съесть как можно больше еды",
                  "Не натыкайтесь на несъедобные предметы, иначе ваш скор уменьшится",
                  "В конце игры вы получите заработанные очки",
                  "Чтобы выйти из игры нажмите на крестик",
                  "Но очтите, что игра не остановиться если вы ее свернете",
                  "Удачи!!!"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (1440, 800))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pass
                return  # i
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 0 <= event.pos[0] <= 720:
                    GFood.food_image = load_image("bone-3.png")
                    Chel.chel_image = load_image("dog.png")

                else:
                    c += 1
                    total_pers = "cat.png"
                    total_food = "bone-3.png"
        pygame.display.flip()
        clock.tick(FPS)


all_sprites = pygame.sprite.Group()


class Chel(pygame.sprite.Sprite):
    chel_image = load_image(total_pers)

    def __init__(self):
        super().__init__(all_sprites)
        self.image = Chel.chel_image
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


class GFood(pygame.sprite.Sprite):
    food_image = load_image(total_food)
    good_food = 0

    def __init__(self, pos):
        self.good_food = 0
        super().__init__(all_sprites)
        self.image = GFood.food_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        # если ещё в небе
        if not pygame.sprite.collide_mask(self, chel):
            self.rect = self.rect.move(0, STEP)
        else:
            self.rect.x = 1500
            self.rect.y = 900
            self.image = load_image("sOjhw.png")
            GFood.good_food += 1


class BFood(pygame.sprite.Sprite):
    food_image = load_image("poop.png")
    bad_food = 0

    def __init__(self, pos):
        super().__init__(all_sprites)
        self.image = BFood.food_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def update(self):
        # если ещё в небе
        if not pygame.sprite.collide_mask(self, chel):
            self.rect = self.rect.move(0, STEP_BAD)
        else:
            # если падает на игрока
            self.rect.x = 1500
            self.rect.y = 900
            self.image = load_image("sOjhw.png")
            BFood.bad_food += 1


def end_screen():
    # запустим конечную заставку игры
    con = sqlite3.connect("base_yummy.db")
    cur = con.cursor()
    score_yes = cur.execute("SELECT score FROM users").fetchall()
    base3 = [i[0] for i in score_yes]
    cur.execute("SELECT login FROM users")
    flag = False
    for i in base3:
        if i == login:
            flag = True
    if not flag:
        tek_score = 0
    # обновляем скор в базе данных
    new_score = max(GFood.good_food - BFood.bad_food, tek_score)
    cur.execute("""UPDATE users
                    SET score = ? WHERE login LIKE ?""", (new_score, login))
    con.commit()
    intro_text = ["Game over",
                  "СПАСИБО ЗА ИГРУ!!!",
                  "ВАШ СКОР " + str(GFood.good_food - BFood.bad_food) + "/100"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (1440, 800))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return  # i
        pygame.display.flip()
        clock2.tick(FPS)

start_screen()
pygame.init()
running = True
x, y = 0, 0

if c != 0:
    Chel.chel_image = load_image("good_cat.png")
    GFood.food_image = load_image("fish.png")
end_game = 0
chel = Chel()

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
