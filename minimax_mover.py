from bfs_mover import bfs_mover
from config import *

class valued_vector:
    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y
    
    def set_path(self, path):
        self.path = path

    def set_depth(self, depth):
        self.depth = depth

    def set_enemies(self, enemies):
        self.enemies = enemies

class enemy_pos:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.can_move = True

class minimax_mover:
    def __init__(self, game_field, enemies, projectiles):
        self.enemies = enemies
        self.projectiles = projectiles
        self.game_field = game_field
        self.path = []
        self.path_values = []
        self.bfs_mover = bfs_mover(game_field)
    
    def set_goal(self, goal):
        self.bfs_mover.set_goal(goal)

    def set_second_goal(self, goal):
        self.bfs_mover.set_second_goal(goal)
        self.second_goal = goal
        
    def set_target(self, target):
        self.bfs_mover.set_target(target)

    def calculate_path_values(self):
        for i in range(len(self.path), 0, -1):
            self.path_values.append(i * 5)

    def evaluate(self, player_i, player_j, path, enemies, projectiles):
        val = 0
        #target_dist = ((player_i - self.target_i)**2 + (player_j - self.target_j)**2)**(1/2)
        #val += -(target_dist)**2 + self.target_reach_points
        todel = []
        old_len = len(path)
        for dt in range(len(path)):
            if player_i == path[dt][0] and player_j == path[dt][1]:
                val += self.path_values[dt]
                path.pop(dt)
                break
        if old_len == len(path):
            val -= 100
        val += (50 - len(path)) * 300
        for en in enemies:
            dis = ((player_i - en.x)**2 + (player_j - en.y)**2)**0.5
            val += (50 - dis) * (-10)
        return val, path

    def max_el(self, array):
        mx = array[0].value
        for i in range(len(array)):
            if array[i].value >= mx:
                mx = array[i].value
        
        counter = len(array)
        while counter > 0:
            for i in array:
                if i.value != mx:
                    array.remove(i)
                    break
            counter -= 1

    def minimax(self, player_i, player_j, is_min, depth, path, enemies, projectiles):
        if depth == 0:
            value, passed = self.evaluate(player_i, player_j, path.copy(), enemies, projectiles)
            ret = valued_vector(value, player_i, player_j)
            ret.set_depth(depth)
            ret.set_enemies(enemies)
            return ret

        if len(path) == 0:
            ret = valued_vector(99999 + 10 * depth, player_i, player_j)
            ret.set_depth(depth)
            return ret

        if is_min == False: 
            moves = []
            if player_i + 1 < 50 and not(self.game_field[(player_i + 1) * game_field_size_x + player_j].is_wall()):
                value, passed = self.evaluate(player_i + 1, player_j, path.copy(), enemies, projectiles)
                moves.append(valued_vector(value, player_i + 1, player_j))
                moves[-1].set_path(passed)

            if player_i - 1 >= 0 and not(self.game_field[(player_i - 1) * game_field_size_x + player_j].is_wall()):
                value, passed = self.evaluate(player_i - 1, player_j, path.copy(), enemies, projectiles)
                moves.append(valued_vector(value, player_i - 1, player_j))
                moves[-1].set_path(passed)
                
            if player_j + 1 < 50 and not(self.game_field[(player_i) * game_field_size_x + player_j + 1].is_wall()):
                value, passed = self.evaluate(player_i, player_j + 1, path.copy(), enemies, projectiles)
                moves.append(valued_vector(value, player_i, player_j + 1))
                moves[-1].set_path(passed)
             
            if player_j - 1 >= 0 and not(self.game_field[(player_i) * game_field_size_x + player_j - 1].is_wall()):
                value, passed = self.evaluate(player_i, player_j - 1, path.copy(), enemies, projectiles)
                moves.append(valued_vector(value, player_i, player_j - 1))
                moves[-1].set_path(passed)

            self.max_el(moves)

            maxv = valued_vector(-99999, 0, 0)
            for mv in moves:
                dt = self.minimax(mv.x, mv.y, not(is_min), depth - 1, mv.path.copy(), enemies, projectiles)
                if dt.value > maxv.value:
                    maxv = valued_vector(dt.value, mv.x, mv.y)
                    maxv.set_path(mv.path)
            
            return maxv

        elif is_min == True: 
            if len(enemies) == 0:
                return self.minimax(player_i, player_j, is_min, depth - 1, path, enemies, projectiles)
            en_best = []
            for en in enemies:
                
                moves = []
                if en.x + 1 < 50 and not(self.game_field[(en.x + 1) * game_field_size_x + en.y].is_wall()):
                    en_cp = enemies.copy()
                    for eni in en_cp:
                        if eni.x == en.x and eni.y == en.y:
                            eni.x += 1

                    value, passed = self.evaluate(player_i, player_j, path.copy(), en_cp, projectiles)
                    moves.append(valued_vector(value, en.x + 1, en.y))
                    moves[-1].set_path(passed)
                    moves[-1].set_enemies(en_cp)

                if en.x - 1 >= 0 and not(self.game_field[(en.x - 1) * game_field_size_x + en.y].is_wall()):
                    en_cp = enemies.copy()
                    for eni in en_cp:
                        if eni.x == en.x and eni.y == en.y:
                            eni.x -= 1

                    value, passed = self.evaluate(player_i, player_j, path.copy(), en_cp, projectiles)
                    moves.append(valued_vector(value, en.x - 1, en.y))
                    moves[-1].set_path(passed)
                    moves[-1].set_enemies(en_cp)
                
                if en.y + 1 < 50 and not(self.game_field[(en.x) * game_field_size_x + en.y + 1].is_wall()):
                    en_cp = enemies.copy()
                    for eni in en_cp:
                        if eni.x == en.x and eni.y == en.y:
                            eni.y += 1

                    value, passed = self.evaluate(player_i, player_j, path.copy(), en_cp, projectiles)
                    moves.append(valued_vector(value, en.x, en.y + 1))
                    moves[-1].set_path(passed)
                    moves[-1].set_enemies(en_cp)
             
                if en.y - 1 >= 0 and not(self.game_field[(en.x) * game_field_size_x + en.y - 1].is_wall()):
                    en_cp = enemies.copy()
                    for eni in en_cp:
                        if eni.x == en.x and eni.y == en.y:
                            eni.y -= 1

                    value, passed = self.evaluate(player_i, player_j, path.copy(), en_cp, projectiles)
                    moves.append(valued_vector(value, en.x, en.y - 1))
                    moves[-1].set_path(passed)
                    moves[-1].set_enemies(en_cp)
                
                values = []
                for mv in moves:
                    dt = self.minimax(player_i, player_j, not(is_min), depth - 1, mv.path.copy(), mv.enemies.copy(), projectiles)
                    values.append(dt.value)
                
                if len(values) == 0:
                    en_best.append(0)
                else:
                    en_best.append(sum(values) / len(values))

            return valued_vector(player_i, player_j, sum(en_best) / len(en_best))
        
    def get_enemies_pos(self):
        self.enemies_pos = []
        for en in self.enemies:
            self.enemies_pos.append(enemy_pos(en.x, en.y))
            
    def get_projectile_pos(self):
        self.projectiles_pos = []
        for proj in self.projectiles:
            self.projectiles_pos.append(enemy_pos(proj.holder.field_x, proj.holder.field_y))
            
    def move_target(self):
        if len(self.path) == 0:
            self.bfs_mover.find_path()
            self.path = self.bfs_mover.path
            self.calculate_path_values()
       
        pre_target_x = self.bfs_mover.target.x
        pre_target_y = self.bfs_mover.target.y
        self.get_enemies_pos()
        self.get_projectile_pos()
        res = self.minimax(self.bfs_mover.target.x, self.bfs_mover.target.y, False, 4, self.path.copy(), self.enemies_pos, self.projectiles_pos)
        self.path = res.path

        self.bfs_mover.target.change_holder(self.game_field[res.x * game_field_size_x + res.y])

        x_diff = pre_target_x - res.x
        y_diff = pre_target_y - res.y

        return x_diff * 48, y_diff * 48

    def move_enemy(self, enemy):
        if len(self.path) == 0:
            self.bfs_mover.find_path()
            self.path = self.bfs_mover.path
            self.calculate_path_values()
       
        self.get_enemies_pos()
        self.get_projectile_pos()
        res = self.minimax(self.bfs_mover.target.x, self.bfs_mover.target.y, True, 4, self.path.copy(), self.enemies_pos.copy(), self.projectiles_pos)
        en_index = 0
        for i in range(len(self.enemies_pos)):
            if self.enemies_pos[i].x == enemy.x and self.enemies_pos[i].y == enemy.y:
                en_index = i
                break
        enemy.change_holder(self.game_field[res.enemies[en_index].x * game_field_size_x + res.enemies[en_index].y])
        if self.bfs_mover.target.x == self.goal.field_x and self.bfs_mover.target.y == self.goal.field_y:
            self.bfs_mover.target.score.score += 50 