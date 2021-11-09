from mover import mover
from collections import deque
from config import *
import numpy as np

class bfs_mover:
    def __init__(self, game_field):
        self.game_field = game_field
        self.path = []

    def set_goal(self, goal):
        self.goal = goal
        self.second_goal = self.goal

    def set_target(self, target):
        self.target = target

    def set_second_goal(self, goal):
        self.second_goal = goal

    def find_path(self):
        startx = self.target.x
        starty = self.target.y

        targetx = self.goal.field_x
        targety = self.goal.field_y

        if startx == targetx and starty == targety:
            targetx = self.second_goal.field_x
            targety = self.second_goal.field_y

        que = deque()
        visited = np.zeros((game_field_size_x,game_field_size_y))
        paths = []
        for j in range(game_field_size_x*game_field_size_y):
            paths.append([0,0])
        que.append([startx, starty]) 
        while len(que) != 0:
            cur_dot = que.popleft()
            if cur_dot[0] == targetx and cur_dot[1] == targety:
                break

            if self.game_field[cur_dot[0] * game_field_size_x + cur_dot[1]].is_wall():
                continue

            if cur_dot[0] + 1 < game_field_size_x and visited[cur_dot[0] + 1][cur_dot[1]] == 0:
                paths[(cur_dot[0] + 1)*game_field_size_x + cur_dot[1]] = [cur_dot[0], cur_dot[1]]
                visited[cur_dot[0] + 1][cur_dot[1]] = 1
                que.append([cur_dot[0] + 1, cur_dot[1]])
        
            if cur_dot[0] - 1 >= 0 and visited[cur_dot[0] - 1][cur_dot[1]] == 0:
                paths[(cur_dot[0] - 1)*game_field_size_x + cur_dot[1]] = [cur_dot[0], cur_dot[1]]
                visited[cur_dot[0] - 1][cur_dot[1]] = 1
                que.append([cur_dot[0] - 1, cur_dot[1]])

            if cur_dot[1] + 1 < game_field_size_y and visited[cur_dot[0]][cur_dot[1] + 1] == 0:
                paths[(cur_dot[0])*game_field_size_x + cur_dot[1] + 1] = [cur_dot[0], cur_dot[1]]
                visited[cur_dot[0]][cur_dot[1] + 1] = 1
                que.append([cur_dot[0], cur_dot[1] + 1])

            if cur_dot[1] - 1 >= 0 and visited[cur_dot[0]][cur_dot[1] - 1] == 0:
                paths[(cur_dot[0])*game_field_size_x + cur_dot[1] - 1] = [cur_dot[0], cur_dot[1]]
                visited[cur_dot[0]][cur_dot[1] - 1] = 1
                que.append([cur_dot[0], cur_dot[1] - 1])
        curX = targetx
        curY = targety
        self.path = []
        while curX != startx or curY != starty:
            self.path.append([curX, curY])
            curX = paths[curX * game_field_size_x + curY][0]
            curY = paths[curX * game_field_size_x + curY][1]
            x_diff = curX - self.path[-1][0]
            y_diff = curY - self.path[-1][1]
            if x_diff != 0 and y_diff != 0:
                self.path.append([curX, curY - y_diff])
            if curX == 0 and curY == 0:
                break

    def reset_path(self):
        self.path = []
        self.find_path()

    def move_target(self):
        if len(self.path) == 0:
            self.find_path()
            return 0, 0
        x_diff = self.target.x - self.path[-1][0]
        y_diff = self.target.y - self.path[-1][1]
        self.target.change_holder(self.game_field[self.path[-1][0] * game_field_size_x + self.path[-1][1]])
        self.path.pop()
        return x_diff * 48, y_diff * 48