import pygame
from enemy import *
from level_generator import *
from random import randint

class Monster_Generator(pygame.sprite.Sprite):
    def __init__(self, map, pos_x, pos_y, pos_i, pos_j):
        super().__init__()
        self.x = pos_x
        self.y = pos_y
        self.map = map
        self.max_mobs = 3
        self.cur_mobs = 0
        self.image = pygame.image.load("Enemies/Skeleton/spawner.png")
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 4), int(self.image.get_height() * 4)))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.pos_i = pos_i
        self.pos_j = pos_j
        self.mobs_list = pygame.sprite.Group()
        self.spawn_rate = 1
        self.lastr_spawn = 0
        
    def new(self, monster_group, monster_pack):
        self.monster_group = monster_group
        self.monster_pack = monster_pack

    def check_if_killed(self, projectile, projectiles):
        for mob in self.mobs_list:
            col = pygame.sprite.collide_rect(projectile, mob)
            if col == True:
                projectiles.remove(projectile)
                self.mobs_list.remove(mob)
                self.monster_group.remove(mob)
                self.cur_mobs -= 1
                return True
        return False

    def spawn(self,walls):
        if self.cur_mobs == self.max_mobs or (pygame.time.get_ticks() - self.lastr_spawn)/1000 < self.spawn_rate:
            return None
        self.cur_mobs += 1
        newEnemy = Enemy(self.monster_pack, walls, self.rect.x, self.rect.y,self.pos_i, self.pos_j)
        newEnemy.set_speed(randint(1,5))
        self.mobs_list.add(newEnemy)
        self.lastr_spawn = pygame.time.get_ticks()
        return newEnemy
