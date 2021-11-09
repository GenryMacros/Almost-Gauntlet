import pygame 
from config import *

class SurfPart(pygame.sprite.Sprite):
    def __init__(self, image_path, holder):
        super().__init__()
        self.holder = holder
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image , (int(self.image.get_width() * floor_scale), int(self.image.get_height() * floor_scale)))
    
    def draw(self, win):
        win.blit(self.image, (self.holder.game_x, self.holder.game_y)) 