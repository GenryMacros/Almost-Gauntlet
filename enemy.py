import pygame
import numpy as np
import math

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
    def __init__(self, pack,walls, pos_x, pos_y, pos_i, pos_j,lvl_matrix):
        super().__init__()
        self.pack = pack
        self.image = pygame.image.load(pack.idle)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * self.pack.mulx), int(self.image.get_height() * self.pack.muly)))
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        self.pos_i = pos_i
        self.pos_j = pos_j
        self.walls = walls
        self.speed = 8
        self.animCount = 0
        self.turned_left = False
        self.last_search_time = 0
        self.next_tile = []
        self.search_cd = 0.2
        self.path = []
        self.lvl_matrix = lvl_matrix
        self.moving = False
        self.surfcx = 0
        self.surfcy = 0

    def set_speed(self,newspeed):
        self.speed = 8

    def check_wall_collision(self,x, y):
        rect = pygame.Rect(x,y, int(self.image.get_width() * self.pack.mulx),int(self.image.get_height() * self.pack.muly))
        for wall in self.walls:
            if wall.rect.colliderect(rect):
                return True
        return False

    def update(self,player_x, player_y, surfacechx, surfacechy, projectiles):
        if len(projectiles.sprites()) != 0:
            self.search_cd = 0
        else:
            self.search_cd = 0.5
        if True:
            if (pygame.time.get_ticks() - self.last_search_time)/1000 >= self.search_cd or self.last_search_time == 0:
                self.path = a_star(int(self.pos_i/48), int(self.pos_j/48), projectiles, int(abs(player_x)/48), int(abs(player_y)/48), surfacechx, surfacechy, self.lvl_matrix)
                if len(self.path) == 0:
                    return
                self.next_tile = self.path[-1]
                self.last_search_time = pygame.time.get_ticks()
            if self.next_tile[0] + self.surfcx  > self.rect.x and self.check_wall_collision(self.rect.x + self.speed, self.rect.y) == False:
                self.rect.x += self.speed
                self.pos_i  += self.speed
                self.turned_left = True
            elif self.next_tile[0] + self.surfcx  < self.rect.x and self.check_wall_collision(self.rect.x - self.speed, self.rect.y) == False:
                self.rect.x -= self.speed
                self.pos_i  -= self.speed
                self.turned_left = False
            if self.next_tile[1] + self.surfcy > self.rect.y and self.check_wall_collision(self.rect.x, self.rect.y + self.speed) == False:
                self.rect.y += self.speed
                self.pos_j  += self.speed
            elif self.next_tile[1] + self.surfcy < self.rect.y and self.check_wall_collision(self.rect.x, self.rect.y - self.speed) == False:
                self.rect.y -= self.speed
                self.pos_j  -= self.speed
            if in_range(self.rect.x, self.next_tile[0] + self.surfcx, 20) and in_range(self.rect.y, self.next_tile[1] + self.surfcy, 20):
                if len(self.path) == 0:
                    return
                if len(self.path) == 1:
                    self.next_tile = self.path[0]
                    self.path.pop()
                    return
                self.path.pop()
                self.next_tile = self.path[-1]
            self.moving = True
        else:
            self.moving = False
    
    def animate(self,win, player_x, player_y, surfacechx, surfacechy, projectiles):
        self.surfcx = surfacechx
        self.surfcy = surfacechy
        self.update(player_x,player_y, surfacechx, surfacechy, projectiles)
        if self.moving == True:
            if self.animCount + 2 >= 20:
                self.animCount = 0
            img = pygame.image.load(self.pack.walk[self.animCount // 6])
            img = pygame.transform.scale(img, (int(img.get_width() * self.pack.mulx), int(img.get_height() * self.pack.muly)))
            win.blit(pygame.transform.flip(img, self.turned_left, False), (self.rect.x, self.rect.y))
            self.animCount += 1
        else:
            win.blit(pygame.transform.flip(self.image, self.turned_left, False), (self.rect.x, self.rect.y))


def evak_key(dot):
  return dot.cost

def in_range(val1, val2, rn):
    return (val1 - rn) < val2 and (val1 + rn) > val2

class Eval_Dot:
    def __init__(self,x,y,cost):
        self.x = x
        self.y = y
        self.cost = cost
class Dot:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def a_star(startx, starty, projectiles, targetx, targety, surfacechx, surfacechy, lvl_matrix):
    que = []
    visited = np.zeros((50,50))
    paths = []
    for j in range(50*50):
        paths.append(Eval_Dot(0,0,0))
    que.append(Eval_Dot(startx, starty, 0))
    while len(que) != 0:
        que.sort(key = evak_key)
        cur_dot = que[0]
        que.pop(0)
        cur_price = cur_dot.cost
        is_proj_onway = False
        if cur_dot.x == targetx and cur_dot.y == targety:
            break
        for proj in projectiles:
            if abs(int((proj.pos_i )/48)) == cur_dot.x and abs(int((proj.pos_j )/48)) == cur_dot.y:
                is_proj_onway = True
                break
        if is_proj_onway:
            continue
        if cur_dot.x + 1 < 50 and visited[cur_dot.x + 1][cur_dot.y] == 0 and lvl_matrix[cur_dot.x + 1][cur_dot.y] != 1:
            paths[(cur_dot.x + 1)*50 + cur_dot.y] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x + 1][cur_dot.y] = 1
            new_price = cur_price + 10 + math.sqrt((cur_dot.x + 1 - targetx)**2 + (cur_dot.y - targety)**2)
            que.append(Eval_Dot(cur_dot.x + 1, cur_dot.y, new_price))
        
        if cur_dot.x - 1 > 0 and visited[cur_dot.x - 1][cur_dot.y] == 0 and lvl_matrix[cur_dot.x - 1][cur_dot.y] != 1:
            paths[(cur_dot.x - 1)*50 + cur_dot.y] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x - 1][cur_dot.y] = 1
            new_price = cur_price + 10 + math.sqrt((cur_dot.x - 1 - targetx)**2 + (cur_dot.y - targety)**2)
            que.append(Eval_Dot(cur_dot.x - 1, cur_dot.y, new_price))

        if cur_dot.y + 1 < 50 and visited[cur_dot.x][cur_dot.y + 1] == 0 and lvl_matrix[cur_dot.x][cur_dot.y + 1] != 1:
            paths[(cur_dot.x)*50 + cur_dot.y + 1] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x][cur_dot.y + 1] = 1
            new_price = cur_price + 10 + math.sqrt((cur_dot.x - targetx)**2 + (cur_dot.y + 1 - targety)**2)
            que.append(Eval_Dot(cur_dot.x, cur_dot.y + 1, new_price))

        if cur_dot.y - 1 > 0 and visited[cur_dot.x][cur_dot.y - 1] == 0 and lvl_matrix[cur_dot.x][cur_dot.y - 1] != 1:
            paths[(cur_dot.x)*50 + cur_dot.y - 1] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x][cur_dot.y - 1] = 1
            new_price = cur_price + 10 + math.sqrt((cur_dot.x - targetx)**2 + (cur_dot.y - 1 - targety)**2)
            que.append(Eval_Dot(cur_dot.x, cur_dot.y - 1, new_price))

    curX = targetx
    curY = targety
    painted_group = []
    while curX != startx or curY != starty:
        painted_group.append([curX*48,  curY*48])
        curX = paths[curX * 50 + curY].x
        curY = paths[curX * 50 + curY].y
        if curX == 0 and curY == 0:
            break
    return painted_group