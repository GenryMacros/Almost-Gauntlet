from config import *
from SurfacePart import SurfPart 
from Tile import Tile
from random import randint
from monster_generator import Monster_Generator

class Field_Creator:
    def __init__(self, player_controller, field, enemies, projectiles, score):
        self.enemies = enemies
        self.projectiles = projectiles
        self.game_field = field
        self.score = score
        self.init_field()
        player_controller.set_projectile_manager(self.game_field[0].projectiles_g, self.game_field[0].enemies_g)
        self.generate_walls()
        self.generate_surface()
        self.playerx, self.playery = player_controller.find_player_pos()
        self.player_controller = player_controller
        self.generate_chest()
        self.generate_exit()
        self.generate_enemy_spawners()
        

    def init_field(self):
        for i in range(game_field_size_x):
            for j in range(game_field_size_y):
                self.game_field[i * game_field_size_x + j] = Tile(i, j, self.score)
                self.game_field[i * game_field_size_x + j].set_sources(self.enemies, self.projectiles)
                self.game_field[i * game_field_size_x + j].set_game_pos(48*i, 48*j)
                self.game_field[i * game_field_size_x + j].make_wall()
                self.game_field[i * game_field_size_x + j].set_sources(self.enemies, self.projectiles)
        
    def generate_walls(self):
        free_tiles = 2400
        counter = 0
        x, y, direction = self.change_dir()
        startx, starty = 25, 25
        while True:
            if counter > free_tiles:
                break
            x, y, direction = self.change_dir()
            while startx + x*direction == 49 or startx + x*direction == 0 or starty + y*direction == 49 or starty + y*direction == 0:
                x, y, direction = self.change_dir()
            startx += x*direction
            starty += y*direction
            self.game_field[startx * game_field_size_x + starty].iswall = False
            counter += 1

    def change_dir(self):
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

    def generate_surface(self):
        for i in range(0, game_field_size_x * 16 * floor_scale, 16 * floor_scale):
            for j in range(0, game_field_size_y * 16 * floor_scale, 16 * floor_scale):
                x_index = int(i/(16 * floor_scale))
                y_index = int(j/(16 * floor_scale))
                if self.game_field[x_index * game_field_size_x + y_index].is_wall():
                    surface_part = SurfPart(wall_path, self.game_field[x_index * game_field_size_x + y_index])
                    self.game_field[x_index * game_field_size_x + y_index].contained_objects.append(surface_part)
                else:
                    surface_part = SurfPart(floors[randint(0, 7)], self.game_field[x_index * game_field_size_x + y_index])
                    self.game_field[x_index * game_field_size_x + y_index].contained_objects.append(surface_part)

    def generate_chest(self):
        for i in range(50):
            for j in range(49,0,-1):
                if not(self.game_field[i * game_field_size_x + j].is_wall()):
                    x = (i + 1) - self.playerx
                    y = (j + 1) - self.playery
                    dis = ((x*x) + (y*y))**(0.5)
                    if dis > 25:
                        chest = SurfPart(chest_path, self.game_field[i * game_field_size_x + j])
                        self.game_field[i * game_field_size_x + j].contained_objects.append(chest)
                        self.chest_pos = [i, j]
                        return
    
    def generate_exit(self):
        for i in range(50):
            for j in range(50):
                if not(self.game_field[i * game_field_size_x + j].is_wall()):
                    x = (i + 1) - self.chest_pos[0]
                    y = (j + 1) - self.chest_pos[1]
                    dis = ((x*x) + (y*y))**(0.5)
                    if dis > 20:
                        exit = SurfPart(exit_path, self.game_field[i * game_field_size_x + j])
                        self.game_field[i * game_field_size_x + j].contained_objects.append(exit)
                        self.exit_pos = [i, j] 
                        return

    def generate_enemy_spawners(self):
        generators_count = enemy_generators_count
        for i in range(50):
            for j in range(50):
                if randint(0, 10) == 10 and not(self.game_field[i * game_field_size_x + j].is_wall()):
                    generators_count -= 1
                    self.game_field[i * game_field_size_x + j].contained_objects.append(Monster_Generator(
                        self.game_field[i * game_field_size_x + j], self.game_field, self.player_controller.player))
                    if generators_count == 0:
                        return