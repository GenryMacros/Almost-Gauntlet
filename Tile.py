import pygame 
from config import *
from projectile import Projectile
from enemy import Enemy

class Tile(pygame.sprite.Sprite):
    def __init__(self, field_x, field_y, score):
        super().__init__()

        self.contained_objects = []
        self.enemies = []
        self.projectiles = []
        self.iswall = False
        self.field_x = field_x
        self.field_y = field_y
        self.score = score

        #self.enemies_g = pygame.sprite.Group()
        #self.projectiles_g = pygame.sprite.Group()

    def set_sources(self, enemies_g, projectiles_g):
        self.enemies_g = enemies_g
        self.projectiles_g = projectiles_g

    def set_game_pos(self, x, y):
        self.game_x = x
        self.game_y = y

    def is_contains_enemies(self):
        return len(self.enemies) > 0

    def is_contains_projectiles(self):
        return len(self.projectiles) > 0

    def add_enemy(self, enemy):
        self.contained_objects.append(enemy)
        self.enemies.append(enemy)
        self.enemies_g.add(enemy)

    def kill_enemy(self):
        if not(self.is_contains_enemies()) or not(self.is_contains_projectiles()):
            return False
        self.remove_projectile()
        self.remove_enemy()
        self.score.score += 5
        return True
        
    def remove_projectile(self):
        if not(self.is_contains_projectiles()):
            return False
        proj = self.projectiles.pop()
        self.contained_objects.remove(proj)
        self.projectiles_g.remove(proj)
        return True

    def remove_enemy(self):
        if not(self.is_contains_enemies()):
            return False
        en = self.enemies.pop()
        self.contained_objects.remove(en)
        self.enemies_g.remove(en)
        en.die()
        return True

    def is_wall(self):
        return self.iswall
    
    def make_wall(self):
        self.iswall = True
    
    def draw(self, win):
        for item in self.contained_objects:
            item.draw(win)