# import os
# import pygame
# from pygame import font
#
# game_folder = os.path.dirname(__file__)
# head, tail = os.path.split(game_folder)
# img_folder = os.path.join(head, "img")
# sound_folder = os.path.join(head, "sounds")
# explosions_img = os.path.join(img_folder, "explosions")
# print(explosions_img)
#
# explosion_anim = {}
# explosion_anim['lg'] = []
# for i in range(9):
#     filename = f'regularExplosion0{i}.png'
#     img = os.path.join(explosions_img, filename)
#     explosion_anim['lg'].append(img)
# print(explosion_anim)

import pygame
import random
import os

from pygame import font

game_folder = os.path.dirname(__file__)
print(game_folder)
head, tail = os.path.split(game_folder)
img_folder = os.path.join(head, "img")
mob_folder = os.path.join(img_folder, "meteors")
sound_folder = os.path.join(head, "sounds")
explosions_img = os.path.join(img_folder, "explosions")
explosions2_img = os.path.join(img_folder, "explosions2")
print(explosions2_img)