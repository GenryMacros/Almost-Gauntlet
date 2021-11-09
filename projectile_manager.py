import pygame
from config import *
from projectile import Projectile

class vector2i:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class projectile_manager:
    def __init__(self, target, projectiles, game_field, enemies):
        self.target = target
        self.projectiles = projectiles
        self.game_field = game_field
        self.enemies = enemies
        #self.generators = generators

    def check_for_targets(self):
        rect = vector2i(self.target.x, self.target.y)
        while rect.x < 50:
            if self.game_field[rect.x * game_field_size_x + rect.y].is_wall():
                break

            if self.game_field[rect.x * game_field_size_x + rect.y].is_contains_enemies():
                return True, 1, 0
            rect.x += 1
    
        rect = vector2i(self.target.x, self.target.y)
        while rect.x >= 0:
            if self.game_field[rect.x * game_field_size_x + rect.y].is_wall():
                break

            if self.game_field[rect.x * game_field_size_x + rect.y].is_contains_enemies():
                return True, -1, 0
            rect.x -= 1

        rect = vector2i(self.target.x, self.target.y)
        while rect.y < 50:
            if self.game_field[rect.x * game_field_size_x + rect.y].is_wall():
                break

            if self.game_field[rect.x * game_field_size_x + rect.y].is_contains_enemies():
                return True, 0, 1
            rect.y += 1

        rect = vector2i(self.target.x, self.target.y)
        while rect.y >= 0:
            if self.game_field[rect.x * game_field_size_x + rect.y].is_wall():
                break
                
            if self.game_field[rect.x * game_field_size_x + rect.y].is_contains_enemies():
                return True, 0, -1
            rect.y -= 1
        return False, 0, 0

    def create(self):
        can_kill, x_mod, y_mod = self.check_for_targets()
        if not(can_kill):
            return
        self.projectiles.add(Projectile(x_mod, y_mod, self.game_field, self.target.holder))
