# shmup game

# rotation works for pygame
# if you rotate directly, each rotation leads to loss of pixels
# therefore create an original and a copy
# rotate the original image in the rotate
"""
new_image = pygame.transform.rotate(self.image_orig, self.rot)
old_center = self.rect.center
self.image = new_image
self.rect.center = old_center ( center has to be the same even with the rotation to reduce the wiggle)
"""


import pygame
import random
import os

game_folder = os.path.dirname(__file__)
head, tail = os.path.split(game_folder)
img_folder = os.path.join(head, "img")

WIDTH = 480
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialise pygame and create window
pygame.init()
pygame.mixer.init()  # for music
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotate!")
clock = pygame.time.Clock()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(player_img, (50, 38))
        # self.image_orig.fill(GREEN)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2  # placement of the rect in x-axis, centerx is a rect command
        self.rect.bottom = HEIGHT / 2  # placement of the rect in y_axis
        self.speed_x = 0  # since we are moving it side to side, we only need speed in x, starting at 0 and updating

        self.rot = 0
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
        self.rotate()  # provide the def


player_img = pygame.image.load(os.path.join(img_folder, 'playerShip1_orange.png')).convert()

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)  # add sprites in all_sprites so that they get updated in the animation, where we update all_sprites

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Update
    all_sprites.update()

    # render/Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    # draw_shield_bar(surf, x, y, pct):
    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
