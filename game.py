import pygame, sys
import enemy
from Tile import Tile
from field_creator import Field_Creator
from player_controller import player_controller
from config import *
from bfs_mover import bfs_mover
from minimax_mover import minimax_mover

class score:
    def __init__(self):
        self.score = 0

class Game:
    def __init__(self):
        pygame.init()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.score = score()

        self.game_field = [Tile(0,0,self.score)] * game_field_size_y * game_field_size_x
        player_mover = minimax_mover(self.game_field, self.enemies, self.projectiles)
        self.player_controller = player_controller(self.game_field, player_mover)
        self.field_creator = Field_Creator(self.player_controller, self.game_field, self.enemies, self.projectiles, self.score)
        player_mover.set_target(self.player_controller.player)
        player_mover.set_goal(self.game_field[game_field_size_x * self.field_creator.chest_pos[0] + self.field_creator.chest_pos[1]])
        player_mover.set_second_goal(self.game_field[game_field_size_x * self.field_creator.exit_pos[0] + self.field_creator.exit_pos[1]])
        self.clock = pygame.time.Clock()
        self.window = pygame.display.set_mode((win_width, win_height))
        pygame.display.set_caption("Gauntlet_Refactored")

        self.isChestCollected = False

    def run(self):
        self.is_running = True
        self.is_won = False
        while self.is_running:
            self.clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
            self.window.fill((0,0,0))
            result = self.player_controller.update()
            if result == True:
                self.is_won = True
                self.is_running = False
            if self.player_controller.player.is_dead():
                self.is_won = False
                self.is_running = False
            for tile in self.game_field:
                tile.draw(self.window)
            pygame.display.update()
        return self.is_won, self.player_controller.player.health, self.player_controller.is_chest_taken