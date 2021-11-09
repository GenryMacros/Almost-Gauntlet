from config import *
import pygame
from random import randint
from bfs_mover import bfs_mover

class Enemy(pygame.sprite.Sprite):
    def __init__(self, holder, game_field, monster_generator, player):
        super().__init__()
        self.holder = holder
        self.monster_generator = monster_generator
        self.holder.add_enemy(self)
        self.x = holder.field_x
        self.y = holder.field_y
        self.index = len(holder.contained_objects) - 1
        self.image = pygame.image.load(skeleton_path)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * skeleton_mul_x), int(self.image.get_height() * skeleton_mul_y)))
        self.player = player
        self.game_field = game_field

        self.mover = bfs_mover(game_field)
        self.mover.set_goal(player)
        self.mover.set_target(self)

        self.move_cd = 0
        self.last_move = 0
        self.is_random = False

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_holder_index(self, index):
        self.index = index

    def make_random(self):
        self.is_random = True

    def change_holder(self, new_holder):
        self.holder.contained_objects.remove(self)
        self.holder.enemies.remove(self)
        new_holder.add_enemy(self)
        self.holder = new_holder
        self.set_holder_index(len(new_holder.contained_objects) - 1)
        self.set_position(self.holder.field_x, self.holder.field_y)

    def die(self):
        if self.is_random:
            self.monster_generator.kill_random_enemy()
        else:
            self.monster_generator.kill_enemy()

    def attack_player(self):
        if self.player.holder.field_x == self.holder.field_x and self.player.holder.field_y == self.holder.field_y:
            self.player.take_damage(5)

    def make_random_move(self):
        while True:
            move = randint(0, 3)
            if  move == 0:
                if self.holder.field_x + 1 >= game_field_size_x:
                    continue
                new_target = self.game_field[(self.holder.field_x + 1) * game_field_size_x + self.holder.field_y]

                if new_target.is_wall():
                    continue
                self.change_holder(new_target)
                break

            elif move == 1:
                if self.holder.field_x - 1 < 0:
                    continue
                new_target = self.game_field[(self.holder.field_x - 1) * game_field_size_x + self.holder.field_y]

                if new_target.is_wall():
                    continue
                self.change_holder(new_target)
                break

            elif move == 2:
                if self.holder.field_y + 1 >= game_field_size_y:
                    continue
                new_target = self.game_field[(self.holder.field_x) * game_field_size_x + self.holder.field_y + 1]

                if new_target.is_wall():
                    continue
                self.change_holder(new_target)
                break

            elif move == 3:
                if self.holder.field_y - 1 < 0:
                    continue
                new_target = self.game_field[(self.holder.field_x) * game_field_size_x + self.holder.field_y - 1]

                if new_target.is_wall():
                    continue
                self.change_holder(new_target)
                break
        
    def draw(self, win):
        if (pygame.time.get_ticks() - self.last_move)/1000 >= self.move_cd:
            if self.is_random == False:
                self.mover.reset_path()
                self.mover.move_target()
                self.last_move = pygame.time.get_ticks()
            else:
                self.make_random_move()

        self.attack_player()
        win.blit(self.image, (self.holder.game_x, self.holder.game_y)) 