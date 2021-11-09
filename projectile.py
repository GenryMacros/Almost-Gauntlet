import pygame
from player_config import *
from config import *

def resize(image):
    return pygame.transform.scale(image, (int(image.get_width() * player_sprite_scale_x), int(image.get_height() * player_sprite_scale_y)))

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x_mod, y_mod, game_field, holder):
        super().__init__()
        self.x_mod = x_mod
        self.y_mod = y_mod

        self.image = pygame.image.load(projectile_default)
        self.image = resize(self.image)

        self.game_field = game_field
        self.holder = holder
        self.holder.contained_objects.append(self)
        self.holder.projectiles.append(self)
    
    def set_position(self, x, y):
        self.x = x
        self.y = y
    
    def set_holder_index(self, index):
        self.index = index

    def change_holder(self, new_holder):
        self.holder.contained_objects.remove(self)
        self.holder.projectiles.remove(self)
        new_holder.contained_objects.append(self)
        new_holder.projectiles.append(self)
        self.holder = new_holder
        self.set_holder_index(len(new_holder.contained_objects) - 1)
        self.set_position(self.holder.field_x, self.holder.field_y)

    def move(self):
        if self.holder.field_x + self.x_mod >= game_field_size_x or self.holder.field_y + self.y_mod >= game_field_size_y or self.holder.is_wall():
            self.holder.contained_objects.remove(self)
            self.holder.projectiles.remove(self)
            return True
        new_holder = self.game_field[(self.holder.field_x + self.x_mod) * game_field_size_x + self.holder.field_y + self.y_mod] 
        self.change_holder(new_holder)
        return self.holder.kill_enemy() or self.holder.is_wall()

    def draw(self, win):
        is_hitted = self.move()
        if not(is_hitted):
            win.blit(self.image, (self.holder.game_x, self.holder.game_y))