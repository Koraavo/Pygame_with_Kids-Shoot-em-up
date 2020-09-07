# shmup game
# Frozen Jam by tgfcoder <https://twitter.com/tgfcoder> licensed under CC-BY-3
# Art from Kenney
# game_over_Screen


import pygame
import random
import os

from pygame import font

game_folder = os.path.dirname(__file__)
# head, tail = os.path.split(game_folder)
img_folder = os.path.join(game_folder, "img")
mob_folder = os.path.join(img_folder, "meteors")
sound_folder = os.path.join(game_folder, "sounds")
explosions_img = os.path.join(img_folder, "explosions")
explosions2_img = os.path.join(img_folder, "explosions2")
powerups_folder = os.path.join(img_folder, 'powerups')

# print(img_folder)s

WIDTH = 480
HEIGHT = 600
FPS = 60
POWERUP_TIME = 5000

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialise pygame and create window
pygame.init()
pygame.mixer.init()  # for music
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shmup!")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial_bold')


def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)  # true anti-aliases the font
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)


def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i  # placement of all the miniatures, since width of each small mini is 25, 5 px space betwen each
        img_rect.y = y
        surf.blit(img, img_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        # self.image.fill(GREEN)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2  # placement of the rect in x-axis
        self.rect.bottom = HEIGHT - 10  # placement of the rect in y_axis
        self.speed_x = 0  # since we are moving it side to side, we only need speed in x, starting at 0 and updating
        self.shield = 100
        self.shoot_delay = 250  # in milliseconds
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # timeout for powerups
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()
        # is it time to unhide?
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 2000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2  # placement of the rect in x-axis
            self.rect.bottom = HEIGHT - 10  # placement of the rect in y_axis
        self.speed_x = 0  # whatever you do do not move until the key is pressed
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0


    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                # placement of x is center x, bottom of the bullet, at the top of the player
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()

    def hide(self):
        # hide the player temporarily
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)



class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        # self.image.fill(RED)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speed_y = random.randrange(1, 8)
        self.speed_x = random.randrange(-2, 2)
        self.rot = 0  # rotation
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.y += self.speed_y
        self.rect.x += self.speed_x
        if self.rect.top > HEIGHT + 30 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-150, -100)
            self.speed_y = random.randrange(1, 8)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        # self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x  # the bullets come from the centre of the player
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center  # the bullets come from the centre of the player
        self.speed_y = 5

    def update(self):
        self.rect.y += self.speed_y
        # kill if it moves off the top of the screen
        if self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):  # where to appear - center, what size explosion - lg or sm
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        # image = explosion_anim['lg'/'sm'][0 = 'lg'] # choose explosion_size['lg']
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()  # get_rect as per the size i.e large or small
        self.rect.center = center  # settings rect's center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75  # speed of the explosion as per the frame_rate

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, 'SCHMUP!', 64, WIDTH/2, HEIGHT/ 4)
    draw_text(screen, "Arrow Keys move, Space to fire", 22, WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "Press a key to begin", 18, WIDTH /2, HEIGHT* 3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# load all game graphics
background = pygame.image.load(os.path.join(img_folder, 'starfield.png')).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_orange.png')).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
# meteor_img = pygame.image.load(os.path.join(img_folder, 'meteorBrown_med1.png')).convert()
bullet_img = pygame.image.load(os.path.join(img_folder, 'laserRed16.png')).convert()

meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_big2.png',
               'meteorBrown_med1.png', 'meteorBrown_med3.png',
               'meteorBrown_small1.png', 'meteorBrown_small2.png',
               'meteorBrown_tiny1.png', 'meteorBrown_tiny2.png']

for img in meteor_list:
    meteor_images.append(pygame.image.load(os.path.join(mob_folder, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):
    filename = f'regularExplosion0{i}.png'
    img = pygame.image.load(os.path.join(explosions_img, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename1 = f'sonicExplosion0{i}.png'
    img2 = pygame.image.load(os.path.join(explosions2_img, filename1)).convert()
    img2.set_colorkey(BLACK)
    explosion_anim['player'].append(img2)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(os.path.join(powerups_folder, 'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(os.path.join(powerups_folder, 'bolt_gold.png')).convert()

# load all game sounds
shoot_sound = pygame.mixer.Sound(os.path.join(sound_folder, 'laser_shot.ogg'))
shield_sound = pygame.mixer.Sound(os.path.join(sound_folder, 'pow4.wav'))
gun_sound = pygame.mixer.Sound(os.path.join(sound_folder, 'pow5.wav'))
expl_sounds = []
for snd in ['Explosion.wav', 'Explosion2.wav']:
    expl_sounds.append(pygame.mixer.Sound(os.path.join(sound_folder, snd)))
player_die_sound = pygame.mixer.Sound(os.path.join(sound_folder, 'rumble1.ogg'))
pygame.mixer.music.load(os.path.join(sound_folder, 'frozenjam.mp3'))
pygame.mixer.music.set_volume(0.4)

pygame.mixer.music.play()
# Game loop
game_over = True
running = True
while running:
    if game_over:
        # all sprite groups
        all_sprites = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        mobs = pygame.sprite.Group()
        for i in range(15):
            newmob()
        # initiating a score
        score = 0


        show_go_screen()
        game_over = False
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update()
    # after the sprites are updated:

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        # for the score (big meteor has a radius close to 43 a nd small close to 8)
        # more points for hitting a small one
        score += 50 - hit.radius
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newmob()

    # check if the mob hit the player
    # if the player is colliding the mobs(group) and mobs to be deleted(True or False) ?
    # pygame uses rectangle as collision by default, specifying using the last argument to use a circle
    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # collision check if player hit a powerup
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            shield_sound.play()
        if player.shield >= 100:
            player.shield = 100

        if hit.type == 'gun':
            player.powerup()
            gun_sound.play()

    # if the player died and the explosion has finished
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # render/Draw
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 20, WIDTH / 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives, player_mini_img)

    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
