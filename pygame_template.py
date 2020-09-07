# basic pygame template includes the following

# width, height, fps, basic colors for the setup of the screen
# initialise the game by creating window
    # pygame.init()
    # init for the music with mixer
    # name of the game
    # clock for the fps
    # update all sprites as a group, instead of individual sprites using all_sprites = pygame.sprite.Group()

# Game Loop
# while running:
    # keep loop at the right speed with FPS

    # process input
        # key press
    # Update all sprites using all_sprites.update()
    # Draw/Render
        # Draw screen
        # draw sprite

        # flip display after everything is drawn


import pygame
import random



WIDTH = 360
HEIGHT = 480
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# initialise pygame and create window
pygame.init()
pygame.mixer.init()  # for music
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()


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
    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
