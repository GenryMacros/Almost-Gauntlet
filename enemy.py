import pygame


class Skelet_Pack:
    def __init__(self):
        self.mulx = 1.7
        self.muly = 1.7
        self.idle = 'Enemies/Skeleton/idle.png'
        self.walk = [
        'Enemies/Skeleton/Move/0.png',
        'Enemies/Skeleton/Move/1.png',
        'Enemies/Skeleton/Move/2.png',
        'Enemies/Skeleton/Move/3.png']

        self.sleep = [
        'Enemies/Skeleton/Sleep/0.png',
        'Enemies/Skeleton/Sleep/0.png',
        'Enemies/Skeleton/Sleep/0.png',
        'Enemies/Skeleton/Sleep/0.png']


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pack,walls, pos_x, pos_y):
        super().__init__()
        self.pack = pack
        self.image = pygame.image.load(pack.idle)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.pack.mulx), int(self.image.get_height() * self.pack.muly)))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.walls = walls
        self.speed = 3
        self.animCount = 0
        self.turned_left = False
    def set_speed(self,newspeed):
        self.speed = newspeed
    def check_wall_collision(self,x, y):
        rect = pygame.Rect(x,y, int(self.image.get_width() * self.pack.mulx),int(self.image.get_height() * self.pack.muly))
        for wall in self.walls:
            if wall.rect.colliderect(rect):
                return True
        return False

    def update(self,player_x,player_y):
        if (((player_x - self.rect.x)**2 + (player_y - self.rect.y)**2)**(1/2)) <= 600:
            if player_x > self.rect.x and self.check_wall_collision(self.rect.x + self.speed, self.rect.y) == False:
                self.rect.x += self.speed
                self.turned_left = True
            elif player_x < self.rect.x and self.check_wall_collision(self.rect.x - self.speed, self.rect.y) == False:
                self.rect.x -= self.speed
                self.turned_left = False
            if player_y > self.rect.y and self.check_wall_collision(self.rect.x, self.rect.y + self.speed) == False:
                self.rect.y += self.speed
            elif player_y < self.rect.y and self.check_wall_collision(self.rect.x, self.rect.y - self.speed) == False:
                self.rect.y -= self.speed
            self.moving = True
        else:
            self.moving = False
    
    def animate(self,win, player_x, player_y):
        self.update(player_x,player_y)
        if self.moving == True:
            if self.animCount + 2 >= 20:
                self.animCount = 0
            img = pygame.image.load(self.pack.walk[self.animCount // 6])
            img = pygame.transform.scale(img, (int(img.get_width() * self.pack.mulx), int(img.get_height() * self.pack.muly)))
            win.blit(pygame.transform.flip(img, self.turned_left, False), (self.rect.x, self.rect.y))
            self.animCount += 1
        else:
            win.blit(pygame.transform.flip(self.image, self.turned_left, False), (self.rect.x, self.rect.y))