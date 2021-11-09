from config import *
from enemy import Enemy
import pygame

class Monster_Generator(pygame.sprite.Sprite):
    def __init__(self, holder, game_field, player):
        super().__init__()
        self.holder = holder
        self.game_field = game_field
        self.player = player

        self.image = pygame.image.load(skeleton_spawner_path)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 4), int(self.image.get_height() * 4)))

        self.spawned_count = 0
        self.random_count = 0
        self.max_spawns = max_spawns

        self.spawn_rate = enemy_spawn_rate
        self.last_spawn = 0

        self.random_enemies = random_enemies_per_spawner
    
    def kill_enemy(self):
        self.spawned_count -= 1
    
    def kill_random_enemy(self):
        self.spawned_count -= 1
        self.random_count -= 1

    def update(self):
        if self.spawned_count == self.max_spawns or (pygame.time.get_ticks() - self.last_spawn)/1000 < self.spawn_rate:
            return 
        self.spawned_count += 1
        newEnemy = Enemy(self.holder, self.game_field, self, self.player)
        if self.random_count != self.random_enemies:
            self.random_count += 1
            newEnemy.make_random()
        self.lastr_spawn = pygame.time.get_ticks()

    def draw(self, win):
        self.update()
        win.blit(self.image, (self.holder.game_x, self.holder.game_y))