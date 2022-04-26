import sys, pygame
pygame.init()

play = True
startGoombas = True
win = True
startTime = pygame.time.get_ticks();
pygame.mixer.music.load('mario.wav')
pygame.mixer.music.play(-1)
img = pygame.image.load('gameOver.png')
play_again = pygame.image.load('playAgain.png')
winner = pygame.image.load('winner1.png')

size = width, height = 640, 480
speed = [1, 1]
black = 0, 0, 0
white = 255, 255, 255
blue = 0, 0, 255
green = 0, 255, 0
lawngreen = 124, 252, 0
red = 255, 0, 0
yellow = 255, 255, 0
orange = 255, 196, 0
pink = 255, 105, 180
purple = 128 ,0 ,128
turquoise = 0, 199, 140
silver = 211, 211, 211
brown = 139, 69, 19

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Rolling Landscape")

playcount = 0

class SpriteSheet(object):
    def __init__(self, filename, color_key=None):
        self.sprite_sheet = pygame.image.load(filename).convert()
        if color_key != None:
            self.sprite_sheet.set_colorkey(color_key)

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height],pygame.SRCALPHA,32).convert_alpha()
        image.blit(self.sprite_sheet, (0,0), (x, y, width, height))
        return image

# Tree Sprite Info
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 1
        self.vel_y = 1
        self.w = w
        self.h = h
        pygame.draw.rect(self.image, (139, 69, 19),
                         [self.w /2 - 5,
                          self.h / 3,
                          10, 2 * self.h / 3])
        pygame.draw.circle(self.image, green,
                           [int(self.w /2),
                            int(self.h /3)],
                           int(self.w / 2 - 5))
        pygame.draw.circle(self.image, black,
                           [int(self.w / 2),
                            int(self.h / 3)],
                        int(self.w / 2- 5), 1)

    def update(self):
        self.rect.x += self.vel_x

        if self.rect.x > width:
            self.rect.x = -self.w - 20

# Cloud Sprite Info
class Blocktwo(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 2
        self.w = w
        self.h = h
        #pygame.draw.rect(self.image, black, [0,0, w, h])
        pygame.draw.circle(self.image, silver,
                           [int(self.w/2),
                            int(self.h/3)],
                           int(self.w /2 - 5))


    def update(self):
        self.rect.x += self.speed_x

        if self.rect.x >= width:
            self.rect.x = -self.w - randrange(0, 50)
            self.rect.y = randrange(0, height//3)

# Mario Sprite Info
class Mario(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.w = w
        self.h = h
        self.r_frames = []
        self.l_frames = []

        sprite_sheet = SpriteSheet("./newMario.png", white)
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(0, 170, 36, 34), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(36, 170, 36, 34), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(72, 170, 36, 34), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(108, 170, 36, 34), (w, h)))
        # 0, 170, 36, 34
        # 36, 170, 36, 34)
        # 72, 170, 36, 34
        # 108, 170, 36, 34
        self.animCount = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x >= width:
            self.rect.x = -self.w - randrange(0, 50) * -1
        pos = self.rect.x
        if self.animCount >= 0:
            frame = (pos // len(self.r_frames)) % len(self.r_frames)
            self.image = self.r_frames[frame]
            if self.animCount > len(self.r_frames):
                self.animCount = -1
            self.animCount += 1

# Goomba Sprite Info
class Goomba(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 1
        self.speed_y = 1
        self.w = w
        self.h = h
        self.r_frames = []
        self.l_frames = []

        sprite_sheet = SpriteSheet('./goomba.png', white)
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(5, 5, 17, 17), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(22, 5, 18, 17), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(40, 5, 19, 17), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(59, 5, 20, 17), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(79, 5, 19, 17), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(98, 5, 18, 17), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(118, 5, 17, 17), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(135, 5, 19, 17), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(154, 5, 18, 17), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(172, 5, 18, 17), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(190, 5, 17, 17), (w, h)))

        self.animCount = 0

    def update(self):
        self.rect.x += self.speed_x

        if self.rect.x > width:
            self.rect.x = -self.w - 20
        pos = self.rect.x
        if self.animCount >= 0:
            frame = (pos // len(self.r_frames)) % len(self.r_frames)
            self.image = self.r_frames[frame]

# Coin Sprite Info
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h], pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 2
        self.speed_y = 2
        self.w = w
        self.h = h
        self.r_frames = []
        self.l_frames = []
        sprite_sheet = SpriteSheet('./coin.png', black)
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(140, 24, 61, 60), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(201, 24, 58, 60), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(271, 24, 43, 60), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(344, 24, 20, 60), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(396, 24, 42, 60), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(452, 24, 57, 60), (w, h)))

        self.animCount = 0

    def update(self):
        self.rect.x += self.speed_x

        if self.rect.x > width:
            self.rect.x = -self.w - 20
        pos = self.rect.x
        if self.animCount >= 0:
            frame = (pos // len(self.r_frames)) % len(self.r_frames)
            self.image = self.r_frames[frame]

# (Non-Existent) Cheetah Info
class Cheetah(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([w, h])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = 0
        self.speed_y = 0
        self.w = w
        self.h = h
        self.r_frames = []
        self.l_frames = []

        sprite_sheet = SpriteSheet("./cheetahsprite.png", white)
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(0, 0, 512, 256), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(512, 0, 512, 256), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(0, 256, 512, 256), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(512, 256, 512, 256), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(0, 512, 512, 256), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(512, 512, 512, 256), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(0, 768, 512, 256), (w, h)))
        self.r_frames.append(pygame.transform.scale(sprite_sheet.get_image(512, 768, 512, 256), (w, h)))

        self.animCount = 0

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x >= width:
            self.rect.x = -self.w - randrange(0, 50) * -1
        pos = self.rect.x
        if self.animCount >= 0:
            frame = (pos // len(self.r_frames)) % len(self.r_frames)
            self.image = self.r_frames[frame]
            if self.animCount > len(self.r_frames):
                self.animCount = -1
            self.animCount += 1

# God knows what this does
    def move(self, direction):
        if direction == "up":
            self.speed_y = -1 * SPEED
        elif direction == "right":
            self.speed_x = SPEED
        elif direction == "down":
            self.speed_y = SPEED
        elif direction == "left":
            self.speed_x = -1 * SPEED
        elif direction == "stop_v":
            self.speed_x = 0
        elif direction == "stop_h":
            self.speed_y = 0

sprite_list = pygame.sprite.Group()
coin_list = pygame.sprite.Group()
goomba_list = pygame.sprite.Group()
from random import randrange

# Tree For Loop
for i in range(0, 6):
    sprite_list.add(Block(randrange(100, width + 30),
                          randrange(175, height + 30),
                          randrange(40, 60),
                          randrange(60,100)))
# Clouds For Loops
for i in range(0, 1):
    sprite_list.add(Blocktwo(randrange(100, width +100),
                          randrange(0, 75),
                          randrange(40, 60),
                          randrange(60,100)))
for i in range(0, 1):
    sprite_list.add(Blocktwo(randrange(100, width -100),
                          randrange(0, 75),
                          randrange(40, 60),
                          randrange(60,100)))
for i in range(0, 1):
    sprite_list.add(Blocktwo(randrange(100, width -100),
                          randrange(0, 75),
                          randrange(40, 60),
                          randrange(60,100)))
for i in range(0, 1):
    sprite_list.add(Blocktwo(randrange(100, width -100),
                          randrange(0, 75),
                          randrange(40, 60),
                          randrange(60,100)))
for i in range(0, 1):
    sprite_list.add(Blocktwo(randrange(100, width -100),
                          randrange(0, 75),
                          randrange(40, 60),
                          randrange(60,100)))
for i in range(0, 1):
    sprite_list.add(Blocktwo(randrange(100, width -100),
                          randrange(0, 75),
                          randrange(40, 60),
                          randrange(60,100)))
for i in range(0, 1):
    sprite_list.add(Blocktwo(randrange(100, width -100),
                          randrange(0, 75),
                          randrange(40, 60),
                          randrange(60,100)))
for i in range(0, 1):
    sprite_list.add(Blocktwo(randrange(100, width -100),
                          randrange(0, 75),
                          randrange(40, 60),
                          randrange(60,100)))
for i in range(0, 1):
    sprite_list.add(Blocktwo(randrange(100, width -100),
                          randrange(0, 75),
                          randrange(40, 60),
                          randrange(60,100)))
# Coins For Loops
for i in range(0, 30):
    coin_list.add(Coin(randrange(100, width + 100),
                          randrange(225, height - 30),
                          randrange(30, 31),
                          randrange(30,31)))
for i in range(0, 15):
    coin_list.add(Coin(randrange(100, width + 100),
                          randrange(225, height - 30),
                          randrange(30, 31),
                          randrange(30,31)))
for i in range(0, 15):
    coin_list.add(Coin(randrange(100, width + 100),
                          randrange(225, height - 30),
                          randrange(30, 31),
                          randrange(30,31)))
# Goomba For Loops
for i in range(0,6):
    goomba_list.add(Goomba(randrange(100, width + 100),
                          randrange(200, height + 30),
                          randrange(45, 46),
                          randrange(45, 46)))

character_list = pygame.sprite.Group()
character_list.add(Mario(300, 300, 30, 60))
clock = pygame.time.Clock()

# Sound effects and score variable
effect = pygame.mixer.Sound('jump.wav')
score = 0
coin_effect = pygame.mixer.Sound('coin.wav')
death_effect = pygame.mixer.Sound('death.wav')
win_effect = pygame.mixer.Sound('winner.wav')

running = True
while running == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                cheetah = character_list.sprites()[0]
                cheetah.rect.y -= 25
                effect.play()
            elif event.key == pygame.K_DOWN:
                cheetah = character_list.sprites()[0]
                cheetah.rect.y += 25
            elif event.key == pygame.K_RIGHT:
                cheetah = character_list.sprites()[0]
                cheetah.rect.x += 25
            elif event.key == pygame.K_LEFT:
                cheetah = character_list.sprites()[0]
                cheetah.rect.x -= 25
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for sprite in sprite_list.sprites():
                    if sprite.rect.collidepoint(x, y):
                        print("MOUSE DETECTION DETECTED")
                        print("MOUSE DETECTION DETECTED")
    if play == True:
        sprite_list.update()
        character_list.update()
        coin_list.update()
        goomba_list.update()
        cheetah = character_list.sprites()[0]
        good_collisions = pygame.sprite.spritecollide(cheetah, coin_list, True)
        bad_collisions = pygame.sprite.spritecollide(cheetah, goomba_list, False)
        for sprite in good_collisions:
            pygame.mixer.music.set_volume(1)
            coin_effect.play()
            score += 1
            print(score)
            if score >= 50:
                win = False
                play = False
        for sprite in bad_collisions:
            if pygame.time.get_ticks() > startTime + 5000:
                pygame.mixer.music.set_volume(1)
                death_effect.play()
                coin_effect.stop()
                pygame.mixer.music.stop()
                print("Your score is", score)
                play = False

    # draw code
    screen.fill(blue)

    # The sun, mountains, and green grass
    pygame.draw.rect(screen, (210, 105, 30), ((0, 290), (640, 190)))
    pygame.draw.rect(screen, (0, 128, 0), ((0, 240), (640, 50)))
    pygame.draw.polygon(screen, (128, 128, 128), ((0, 240), (120, 120), (240, 240)))
    pygame.draw.polygon(screen, (255, 255, 255), ((120, 120), (160, 160), (80, 160)))
    pygame.draw.polygon(screen, (128, 128, 128), ((240, 240), (360, 120), (480, 240)))
    pygame.draw.polygon(screen, (255, 255, 255), ((360, 120), (320, 160), (400, 160)))
    pygame.draw.circle(screen, yellow, (540, 50), 40)
    sprite_list.draw(screen)
    character_list.draw(screen)
    coin_list.draw(screen)
    goomba_list.draw(screen)
    # Select the font to use, size, bold, italics
    font = pygame.font.SysFont('Calibri', 25, True, False)

    # Render the text. "True" means anti-aliased text.
    # Black is the color. The variable BLACK was defined
    # above as a list of [0, 0, 0]
    # Note: This line creates an image of the letters,
    # but does not put it on the screen yet.
    text = font.render("You have " + str(score) + " Coins", True, black)
    text2 = font.render("You have " + str(score) + " Coins", True, white)
    info = font.render("Get 50 Coins to Win!", True, black)
    info2 = font.render("Goomba registration 5 seconds after start!", True, black)

    # Put the image of the text on the screen at 250x250
    screen.blit(text, [0, 0])
    screen.blit(info, [0, 25])
    screen.blit(info2, [0, 50])

    if not play:
        pygame.draw.rect(screen, black, (0, 0, 640, 480))
        screen.blit(pygame.transform.scale(img, (640, 480)), (0, 0))
        screen.blit(pygame.transform.scale(text2, (100, 25)), (270, 425))

    if not win:
        pygame.draw.rect(screen, black, (0, 0, 640, 480))
        screen.blit(pygame.transform.scale(winner, (640, 480)), (0, 0))
        death_effect.stop()
        if playcount < 1:
            win_effect.play()
            pygame.mixer.music.stop()
            playcount += 1
            if playcount == 1:
                pygame.mixer.music.set_volume(0)

    pygame.display.update()
    clock.tick(60)
