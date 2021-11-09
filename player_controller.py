from config import *
from player import Player
from projectile_manager import projectile_manager

class player_controller:
    def __init__(self, game_field, mover):
        self.game_field = game_field
        self.mover = mover
        self.player = Player(self.game_field[0], game_field)
        self.game_field[0].contained_objects.append(self.player)
        self.player.set_holder_index(len(self.game_field[0].contained_objects) - 1)
        self.is_chest_taken = False

    def set_projectile_manager(self, projectiles_g, enemies_g):
        self.projectile_manager = projectile_manager(self.player, projectiles_g, self.game_field, enemies_g)

    def find_player_pos(self):
        x = 0
        y = 0
        for i in range(0, 50):
            for j in range(0, 50):
                if not(self.game_field[i * game_field_size_x + j].is_wall()):
                    x = i
                    y = j
                    break
        self.player.set_position(x, y)
        self.player.change_holder(self.game_field[x * game_field_size_x + y])
        x *= 48
        y *= 48
        while y > int( win_width/ 2):
            for tile in self.game_field:
                tile.game_y -= 4
            y -= 4
        while x > int(win_height / 2):
            for tile in self.game_field:
                tile.game_x -= 4
            x -= 4
        while y < int( win_width/ 2):
            for tile in self.game_field:
                tile.game_y += 4
            y += 4
        while x < int(win_height / 2):
            for tile in self.game_field:
                tile.game_x += 4
            x += 4
        return self.player.x, self.player.y

    def update(self):
        if self.player.x == self.mover.bfs_mover.goal.field_x and self.mover.bfs_mover.goal.field_y == self.player.y:
            #self.player.holder.contained_objects.pop(len(self.player.holder.contained_objects) - 2)
            self.is_chest_taken = True

        if self.mover.second_goal.field_x == self.player.x and self.mover.second_goal.field_y == self.player.y and self.is_chest_taken == True:
            return True
        x_diff, y_diff = self.mover.move_target()
        self.projectile_manager.create()
        for tile in self.game_field:
            tile.game_x += x_diff
            tile.game_y += y_diff

        return False
