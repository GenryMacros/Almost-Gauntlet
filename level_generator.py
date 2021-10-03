import pygame
import numpy as np
from random import randint
from enemy_generator import *
floor_scale = 3
class SurfPart(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.image = pygame.transform.scale(self.image , (int(self.image.get_width() * floor_scale), int(self.image.get_height() * floor_scale)))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y

floors = [
"Surface/Floor/0.png",
"Surface/Floor/1.png",
"Surface/Floor/2.png",
"Surface/Floor/3.png",
"Surface/Floor/4.png",
"Surface/Floor/5.png",
"Surface/Floor/6.png",
"Surface/Floor/7.png"
]

walls = [
"Surface/Wall/left.png",
"Surface/Wall/right.png",
"Surface/Wall/top.png",
"Surface/Wall/left_top.png",
"Surface/Wall/left_bottom.png",
"Surface/Wall/right_top.png",
"Surface/Wall/right_bottom.png",
"Surface/Wall/top.png"
]



surface = pygame.sprite.Group()
wallsg = pygame.sprite.Group()

min_room_size_x = 4
min_room_size_y = 4
map_size_x = 50 * 16 * floor_scale
map_size_y = 50 * 16 * floor_scale
lvl_matrix = np.ones((50,50))
generators = pygame.sprite.Group()
chestsp = SurfPart("Surface/chest.png",0, 0)
exitsp = SurfPart("Surface/chest.png",0, 0)

def change_dir():
    x = 0
    y = 0
    direction = 1
    if randint(0, 1) == 1:
        x = 1
    else:
        y = 1
    if randint(0, 1) == 1:
        direction = 1
    else:
        direction = -1
    return x, y, direction


def generate_walls_simple(lvl_matrix, free_tiles, startx, starty):
    counter = 0
    x, y, direction = change_dir()

    while True:
        if counter > free_tiles:
            break
        x, y, direction = change_dir()
        while startx + x*direction == 49 or startx + x*direction == 0 or starty + y*direction == 49 or starty + y*direction == 0:
            x, y, direction = change_dir()
        startx += x*direction
        starty += y*direction
        lvl_matrix[startx][starty] = 0
        counter += 1

def re_gen():
    #lvl_matrix = np.ones((50,50))
    generate_walls_simple(lvl_matrix, 2300, 38, 38)

    for i in range(0, map_size_x, 16 * floor_scale):
        for j in range(0, map_size_y, 16 * floor_scale):
            x_index = int(i/(16 * floor_scale))
            y_index = int(j/(16 * floor_scale))
            if lvl_matrix[x_index][y_index] == 0:
                surface_part = SurfPart(floors[randint(0, 7)], i, j)
                surface.add(surface_part)
                if lvl_matrix[x_index - 1][y_index]:
                    surface_part = SurfPart(walls[0], i - 16 * floor_scale, j)
                    wallsg.add(surface_part)
                if lvl_matrix[x_index + 1][y_index]:
                    surface_part = SurfPart(walls[1], i + 16 * floor_scale, j)
                    wallsg.add(surface_part)
                if lvl_matrix[x_index][y_index + 1]:
                    surface_part = SurfPart(walls[7], i, j + 16 * floor_scale)
                    surface_part.image = pygame.transform.flip(
                        surface_part.image, False, True)
                    wallsg.add(surface_part)
                if lvl_matrix[x_index][y_index - 1]:
                    surface_part = SurfPart(walls[2], i, j - 16 * floor_scale)
                    wallsg.add(surface_part)


def spawn_spawners(count):
    for i in range(50):
        for j in range(50):
            if randint(0, 10) == 10 and lvl_matrix[i][j] == 0:
                count -= 1
                lvl_matrix[i][j] = 3
                generators.add(Monster_Generator(
                    lvl_matrix, i*16 * floor_scale, j*16 * floor_scale, i*48,j*48, lvl_matrix))
                if count == 0:
                    return

def spawn_chest(playerx, playery):
    for i in range(50):
        for j in range(49,0,-1):
            if lvl_matrix[i][j] == 0:
                x = (i + 1) - playerx
                y = (j + 1) - playery
                dis = ((x*x) + (y*y))**(0.5)
                if dis > 25:
                    lvl_matrix[i][j] = 2
                    chest = SurfPart("Surface/chest.png",i * 48, j * 48)
                    surface.add(chest)
                    return i,j,chest

def spawn_exit(chestx, chesty):
    for i in range(50):
        for j in range(50):
            if lvl_matrix[i][j] == 0:
                x = (i + 1) - chestx
                y = (j + 1) - chesty
                dis = ((x*x) + (y*y))**(0.5)
                if dis > 20:
                    lvl_matrix[i][j] = 2
                    exit = SurfPart("Surface/ladder.png",i * 48, j * 48)
                    surface.add(exit)
                    return exit,i ,j 