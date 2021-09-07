import pygame

PLAYER_SPEED = 5
sprite_scale_x = 1.7
sprite_scale_y = 1.4

def Scale_arr(arr):
    for i in range(len(arr)):
        arr[i] =  pygame.transform.scale(arr[i], (int(arr[i].get_width() * sprite_scale_x), int(arr[i].get_height() * sprite_scale_y)))

player_idle = pygame.image.load('Player/stay.png')
player_idle = pygame.transform.scale(player_idle, (int(player_idle.get_width() * sprite_scale_x), int(player_idle.get_height() * sprite_scale_y)))
player_walk = [
pygame.image.load('Player/Move/0.png'),
pygame.image.load('Player/Move/1.png'),
pygame.image.load('Player/Move/2.png'),
pygame.image.load('Player/Move/3.png')]

player_sleep = [
pygame.image.load('Player/Sleep/0.png'),
pygame.image.load('Player/Sleep/1.png'),
pygame.image.load('Player/Sleep/2.png'),
pygame.image.load('Player/Sleep/3.png')]

Scale_arr(player_walk)


class Projectile(pygame.sprite.Sprite):
    def __init__(self, picture_path, pos_x, pos_y, is_left, is_up, is_turned_x, is_turned_y):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.image = pygame.transform.scale(self.image , (int(self.image.get_width() * sprite_scale_x), int(self.image.get_height() * sprite_scale_y)))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.is_left = is_left
        self.is_up = is_up
        self.is_turned_x = is_turned_x
        self.is_turned_y = is_turned_y
        if self.is_turned_x == True:
            if self.is_left == True:
                self.image = pygame.transform.rotate(self.image, -90)
                self.image = pygame.transform.flip(self.image, True, False)
            else:
                self.image = pygame.transform.rotate(self.image, -90)
        if self.is_turned_y == True:
            if self.is_up == True:
                pass
            else:
                self.image = pygame.transform.rotate(self.image, 180)
        
    def update(self):
        if self.is_turned_x == True:
            if self.is_left == True:
                self.rect.x -= 10
            else:
                self.rect.x += 10
        if self.is_turned_y == True:
            if self.is_up == True:
                self.rect.y -= 10
            else:
                self.rect.y += 10

        
    def check_collission(self, walls, enemies):
        rect = pygame.Rect(self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height())
        for wall in walls:
            if wall.rect.colliderect(rect):
                return True
        return False

    def draw(self,win):
        self.update()
        win.blit(self.image,(self.rect.x, self.rect.y))