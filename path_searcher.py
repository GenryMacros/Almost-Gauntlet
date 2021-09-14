import pygame
from collections import deque
from level_generator import *
import time
class Dot:
    def __init__(self,x,y):
        self.x = x
        self.y = y

def bfs_search(startx, starty, enemies, targetx, targety,surface,surfacechx,surfacechy):
    que = deque()
    visited = np.zeros((50,50))
    paths = []
    for j in range(50*50):
            paths.append(Dot(0,0))
    que.append(Dot(startx, starty)) 
    while len(que) != 0:
        cur_dot = que.popleft()
        is_enemy_onway = False
        if cur_dot.x == targetx and cur_dot.y == targety:
            break
        for en in enemies:
            if abs(int((en.pos_i)/48)) == cur_dot.x and abs(int((en.pos_j)/48)) == cur_dot.y:
                is_enemy_onway = True
                break
        if is_enemy_onway:
            continue
        if cur_dot.x + 1 < 50 and visited[cur_dot.x + 1][cur_dot.y] == 0 and lvl_matrix[cur_dot.x + 1][cur_dot.y] != 1:
            paths[(cur_dot.x + 1)*50 + cur_dot.y] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x + 1][cur_dot.y] = 1
            que.append(Dot(cur_dot.x + 1, cur_dot.y))
        
        if cur_dot.x - 1 > 0 and visited[cur_dot.x - 1][cur_dot.y] == 0 and lvl_matrix[cur_dot.x - 1][cur_dot.y] != 1:
            paths[(cur_dot.x - 1)*50 + cur_dot.y] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x - 1][cur_dot.y] = 1
            que.append(Dot(cur_dot.x - 1, cur_dot.y))

        if cur_dot.y + 1 < 50 and visited[cur_dot.x][cur_dot.y + 1] == 0 and lvl_matrix[cur_dot.x][cur_dot.y + 1] != 1:
            paths[(cur_dot.x)*50 + cur_dot.y + 1] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x][cur_dot.y + 1] = 1
            que.append(Dot(cur_dot.x, cur_dot.y + 1))

        if cur_dot.y - 1 > 0 and visited[cur_dot.x][cur_dot.y - 1] == 0 and lvl_matrix[cur_dot.x][cur_dot.y - 1] != 1:
            paths[(cur_dot.x)*50 + cur_dot.y - 1] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x][cur_dot.y - 1] = 1
            que.append(Dot(cur_dot.x, cur_dot.y - 1))
    curX = targetx
    curY = targety
    painted_group = pygame.sprite.Group()
    while curX != startx or curY != starty:
        curX = paths[curX * 50 + curY].x
        curY = paths[curX * 50 + curY].y
        if curX == 0 and curY == 0:
            break
        paintd = SurfPart("wall.png", curX * 48 + surfacechx,  curY * 48 + surfacechy)
        surface.add(paintd)
        painted_group.add(paintd)
    return painted_group


def dfs_search(startx, starty, enemies, targetx, targety,surface,surfacechx,surfacechy):
    que = deque()
    visited = np.zeros((50,50))
    paths = []
    for j in range(50*50):
            paths.append(Dot(0,0))
    que.append(Dot(startx, starty)) 
    while len(que) != 0:
        cur_dot = que.pop()
        is_enemy_onway = False
        if cur_dot.x == targetx and cur_dot.y == targety:
            break
        for en in enemies:
            if int(en.pos_i/48) == cur_dot.x and int(en.pos_j/48) == cur_dot.y:
                is_enemy_onway = True
                break
        if is_enemy_onway:
            continue
        if cur_dot.x + 1 < 50 and visited[cur_dot.x + 1][cur_dot.y] == 0 and lvl_matrix[cur_dot.x + 1][cur_dot.y] != 1:
            paths[(cur_dot.x + 1)*50 + cur_dot.y] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x + 1][cur_dot.y] = 1
            que.append(Dot(cur_dot.x + 1, cur_dot.y))
        
        if cur_dot.x - 1 > 0 and visited[cur_dot.x - 1][cur_dot.y] == 0 and lvl_matrix[cur_dot.x - 1][cur_dot.y] != 1:
            paths[(cur_dot.x - 1)*50 + cur_dot.y] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x - 1][cur_dot.y] = 1
            que.append(Dot(cur_dot.x - 1, cur_dot.y))

        if cur_dot.y + 1 < 50 and visited[cur_dot.x][cur_dot.y + 1] == 0 and lvl_matrix[cur_dot.x][cur_dot.y + 1] != 1:
            paths[(cur_dot.x)*50 + cur_dot.y + 1] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x][cur_dot.y + 1] = 1
            que.append(Dot(cur_dot.x, cur_dot.y + 1))

        if cur_dot.y - 1 > 0 and visited[cur_dot.x][cur_dot.y - 1] == 0 and lvl_matrix[cur_dot.x][cur_dot.y - 1] != 1:
            paths[(cur_dot.x)*50 + cur_dot.y - 1] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x][cur_dot.y - 1] = 1
            que.append(Dot(cur_dot.x, cur_dot.y - 1))
    curX = targetx
    curY = targety
    painted_group = pygame.sprite.Group()
    while curX != startx or curY != starty:
        curX = paths[curX * 50 + curY].x
        curY = paths[curX * 50 + curY].y
        if curX == 0 and curY == 0:
            break
        paintd = SurfPart("wall.png", curX * 48 + surfacechx,  curY * 48 + surfacechy)
        surface.add(paintd)
        painted_group.add(paintd)
    return painted_group


def uniform_cost_search(startx, starty, enemies, targetx, targety,surface,surfacechx,surfacechy):
    que = deque()
    visited = np.zeros((50,50))
    cost = np.zeros((50,50))
    cur_best_path = []
    cur_best = 100000000000 
    paths = []
    for j in range(50*50):
            paths.append(Dot(0,0))
    que.append(Dot(startx, starty)) 
    while len(que) != 0:
        cur_dot = que.popleft()
        this_cost = 1
        is_enemy_onway = False
        if cur_dot.x == targetx and cur_dot.y == targety:
            if cur_best > cost[cur_dot.x][cur_dot.y]:
                cur_best = cost[cur_dot.x][cur_dot.y]
                cur_best_path = []
                curX = cur_dot.x
                curY = cur_dot.y
    
                while curX != startx or curY != starty:
                    curX = paths[curX * 50 + curY].x
                    curY = paths[curX * 50 + curY].y
                    cur_best_path.append(Dot(curX,curY))
                continue

        for en in enemies:
            if int(en.pos_i / 48) == cur_dot.x and int(en.pos_j / 48) == cur_dot.y:
                this_cost += 1

        if cur_dot.x + 1 < 50 and visited[cur_dot.x + 1][cur_dot.y] == 0 and lvl_matrix[cur_dot.x + 1][cur_dot.y] != 1:
            paths[(cur_dot.x + 1)*50 + cur_dot.y] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x + 1][cur_dot.y] = 1
            cost[cur_dot.x + 1][cur_dot.y] += this_cost
            que.append(Dot(cur_dot.x + 1, cur_dot.y))
        
        if cur_dot.x - 1 > 0 and visited[cur_dot.x - 1][cur_dot.y] == 0 and lvl_matrix[cur_dot.x - 1][cur_dot.y] != 1:
            paths[(cur_dot.x - 1)*50 + cur_dot.y] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x - 1][cur_dot.y] = 1
            cost[cur_dot.x - 1][cur_dot.y] += this_cost
            que.append(Dot(cur_dot.x - 1, cur_dot.y))

        if cur_dot.y + 1 < 50 and visited[cur_dot.x][cur_dot.y + 1] == 0 and lvl_matrix[cur_dot.x][cur_dot.y + 1] != 1:
            paths[(cur_dot.x)*50 + cur_dot.y + 1] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x][cur_dot.y + 1] = 1
            cost[cur_dot.x][cur_dot.y + 1] += this_cost
            que.append(Dot(cur_dot.x, cur_dot.y + 1))

        if cur_dot.y - 1 > 0 and visited[cur_dot.x][cur_dot.y - 1] == 0 and lvl_matrix[cur_dot.x][cur_dot.y - 1] != 1:
            paths[(cur_dot.x)*50 + cur_dot.y - 1] = Dot(cur_dot.x, cur_dot.y)
            visited[cur_dot.x][cur_dot.y - 1] = 1
            cost[cur_dot.x][cur_dot.y - 1] += this_cost
            que.append(Dot(cur_dot.x, cur_dot.y - 1))
    painted_group = pygame.sprite.Group()
    for dot in cur_best_path:
        paintd = SurfPart("wall.png", dot.x * 48 + surfacechx,  dot.y * 48 + surfacechy)
        surface.add(paintd)
        painted_group.add(paintd)
    return painted_group