import pygame, sys
from player_config import *
from config import *

def resize(image):
    return pygame.transform.scale(image, (int(image.get_width() * player_sprite_scale_x), int(image.get_height() * player_sprite_scale_y)))

class Player(pygame.sprite.Sprite):
    def __init__(self, holder, game_field):
        super().__init__()
        self.holder = holder
        self.game_field = game_field

        self.invulnerability_last = 0
        self.invulnerability_coldown = 0.1

        self.harvest_time_last = 0
        self.harvest_time_coldown = 1

        self.attack_rate = 0.3

        self.health = player_health
        
        self.image = pygame.image.load(player_default)
        self.image = resize(self.image)
        
    def is_dead(self):
        return self.health <= 0

    def take_damage(self, damage):
        if (pygame.time.get_ticks() - self.invulnerability_last)/1000 >= self.invulnerability_coldown:
            self.health -= damage
            self.invulnerability_last = pygame.time.get_ticks()
        
    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_field_position(self):
        self.field_x = self.x
        self.field_y = self.y

    def update(self):
        print(self.health)
        if (pygame.time.get_ticks() - self.harvest_time_last)/1000 >= self.harvest_time_coldown:
            self.health -= 1
            self.harvest_time_last = pygame.time.get_ticks()

    def set_holder_index(self, index):
        self.index = index

    def change_holder(self, new_holder):
        self.holder.contained_objects.remove(self)
        new_holder.contained_objects.append(self)
        self.holder = new_holder
        self.set_holder_index(len(new_holder.contained_objects) - 1)
        self.set_position(self.holder.field_x, self.holder.field_y)
        self.set_field_position()

    def draw(self, win):
        self.update()
        win.blit(self.image, (self.holder.game_x, self.holder.game_y))