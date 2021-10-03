import pygame
from Config import *
from player import *
from level_generator import *

pygame.init()

class Game:
    def __init__(self):
        pygame.init()
        self.win_width = 900
        self.win_height = 700
        self.screen = pygame.display.set_mode((self.win_width, self.win_height))
        self.font = pygame.font.Font("Fonts\EightBitDragon.ttf",25)
        self.running = True
        self.surface = pygame.sprite.Group()
        self.walls  = pygame.sprite.Group()
        self.generators  = pygame.sprite.Group()
        self.enemies  = pygame.sprite.Group()
        self.player_spawn()

    def player_spawn(self):
        surface_change_x = 0
        surface_change_y = 0
        self.x = self.y = 0
        self.xi = self.yi = 0
        for i in range(0, 50):
            for j in range(0, 50):
                if lvl_matrix[i][j] == 0:
                    self.x = (i) * 48
                    self.y = (j) * 48
                    self.xi = self.x
                    self.yi = self.y
                    break       
        self.cx, self.cy, self.chestsp = spawn_chest(self.x/48, self.y/48)
        self.exitsp,self.ex,self.ey = spawn_exit(self.cx, self.cy)
        while self.y > int( self.win_width/ 2):
            for sur in surface: 
                sur.rect.y -= 4
            for wall in wallsg:
                wall.rect.y -= 4
            for gen in generators:
                gen.rect.y -= 4
            self.y -= 4
            surface_change_y -= 4
        while self.x > int(self.win_height / 2):
            for sur in surface:
                sur.rect.x -= 4
            for wall in wallsg:
                wall.rect.x -= 4
            for gen in generators:
                gen.rect.x -= 4
            self.x -= 4
            surface_change_x -= 4
        while self.y < int( self.win_width/ 2):
            for sur in surface:
                sur.rect.y += 4
            for wall in wallsg:
                wall.rect.y += 4
            for gen in generators:
                gen.rect.y += 4
            self.y += 4
            surface_change_y += 4
        while self.x < int(self.win_height / 2):
            for sur in surface:
                sur.rect.x += 4
            for wall in wallsg:
                wall.rect.x += 4
            for gen in generators:
                gen.rect.x += 4
            self.x += 4
            surface_change_x += 4

    def update(self):
        self.all_sprites.update()
        pass

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        pass

    def draw(self):
        self.screen.fill((0,0,0))
        self.player_group.draw(self.screen)
        self.projectiles_group.draw(self.screen)
        self.walls_group.draw(self.screen)
        self.enemies_group.draw(self.screen)
        self.floor_group.draw(self.screen)
        self.clock.tick(30)
        pygame.display.update()

    def main(self):
        while self.running:
            self.events()
            self.update()
            self.draw()
        pass

    def game_over(self):
        pass

    def intro(self):
        pass

gauntlet = Game()
gauntlet.new()
gauntlet.main()
pygame.quit()