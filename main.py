from types import TracebackType
import pygame, sys
import pygame_menu
import os
from datetime import datetime
from player_stuff import *
from level_generator import surface,lvl_matrix,wallsg,generators,spawn_spawners,re_gen,spawn_chest,spawn_exit,clean
import numpy as np
from enemy import *
from path_searcher import *
from agent import *

def check_collision(rect, arr):
        for el in arr:
            if el.rect.colliderect(rect):
                return True
        return False

def get_attack_direction(startx, starty, enemies, walls):
    rect = pygame.Rect(startx, starty, 10, 10)
    while True:
        if check_collision(rect, enemies):
            return 0
        rect.x += 1
        if check_collision(rect, walls):
            break
    rect = pygame.Rect(startx, starty, 10, 10)
    while True:
        if check_collision(rect, enemies):
            return 1
        rect.x -= 1
        if check_collision(rect, walls):
            break

    rect = pygame.Rect(startx, starty, 10, 10)
    while True:
        if check_collision(rect, enemies):
            return 2
        rect.y += 1
        if check_collision(rect, walls):
            break

    rect = pygame.Rect(startx, starty, 10, 10)
    while True:
        if check_collision(rect, enemies):
            return 3
        rect.y -= 1
        if check_collision(rect, walls):
            break
    return -1

pygame.init()
win_width = 480 
win_height = 480
clock = pygame.time.Clock()
win = pygame.display.set_mode((win_width, win_width), 0, 32)
pygame.display.set_caption("Gauntlet_Reforged")
 

def game():
    games_count = 10000
    agent = Agent()
    last_best_result = 0
    record = -500
    while games_count > 0:
        for i in range(50):
            for j in range(50):
                lvl_matrix[i][j] = 1
        clean()
        print(games_count)
        last_best_result = 0
        re_gen()
        font = pygame.font.Font("Fonts/EightBitDragon.ttf", 24)
        score = font.render("Health",True, (255,0,0))
        health = font.render("Score",True, (255,0,0))
        pclass = font.render("Warrior",True, (255,0,0))
        sp_left = font.render("Spawners left",True, (255,0,0))
        alg = font.render("Current algo",True,(255,0,0))
        param_rect = pygame.Rect(610,0, 140,140)
        x = 640
        y = 640
        width = 32
        height = 32
        speed = 5
        health_points = 100

        run = True
        turned_left = False
        turned_up = False
        is_turned_x = True
        is_turned_y = True
        animCount = 0
        generators_count = 5
        surface_change_x = 0
        surface_change_y = 0
        spawn_spawners(generators_count)
        algos = ["bfs","dfs","uniform"]
        current_search_algo = 0
        def change_algo(current_search_algo):
            current_search_algo += 1
            if current_search_algo == 3:
                current_search_algo = 0
            return current_search_algo
        def exec_algo(algo, isChestCollected):
            if algo == "bfs":
                if isChestCollected == False:
                    return bfs_search(int(xi/48),int(yi/48),enemies,cx,cy,surface,surface_change_x,surface_change_y)
                else:
                    return bfs_search(int(xi/48),int(yi/48),enemies,ex,ey,surface,surface_change_x,surface_change_y)
            elif algo == "dfs":
                if isChestCollected == False:
                    return dfs_search(int(xi/48),int(yi/48),enemies,cx,cy,surface,surface_change_x,surface_change_y)
                else:
                    return dfs_search(int(xi/48),int(yi/48),enemies,ex,ey,surface,surface_change_x,surface_change_y)
            elif algo == "uniform":
                if isChestCollected == False:
                    return uniform_cost_search(int(xi/48),int(yi/48),enemies,cx,cy,surface,surface_change_x,surface_change_y)
                else:
                    return uniform_cost_search(int(xi/48),int(yi/48),enemies,ex,ey,surface,surface_change_x,surface_change_y)

        def player_spawn():
            surface_change_x = 0
            surface_change_y = 0
            x = y = 0
            xi = yi = 0
            for i in range(0, 50):
                for j in range(0, 50):
                    if lvl_matrix[i][j] == 0:
                        x = (i) * 48
                        y = (j) * 48
                        xi = x
                        yi = y
                        break       
            cx, cy, chestsp = spawn_chest(x/48, y/48)
            exitsp,ex,ey = spawn_exit(cx, cy)
            while y > int( win_width/ 2):
                for sur in surface: 
                    sur.rect.y -= 4
                for wall in wallsg:
                    wall.rect.y -= 4
                for gen in generators:
                    gen.rect.y -= 4
                y -= 4
                surface_change_y -= 4
            while x > int(win_height / 2):
                for sur in surface:
                    sur.rect.x -= 4
                for wall in wallsg:
                    wall.rect.x -= 4
                for gen in generators:
                    gen.rect.x -= 4
                x -= 4
                surface_change_x -= 4
            while y < int( win_width/ 2):
                for sur in surface:
                    sur.rect.y += 4
                for wall in wallsg:
                    wall.rect.y += 4
                for gen in generators:
                    gen.rect.y += 4
                y += 4
                surface_change_y += 4
            while x < int(win_height / 2):
                for sur in surface:
                    sur.rect.x += 4
                for wall in wallsg:
                    wall.rect.x += 4
                for gen in generators:
                    gen.rect.x += 4
                x += 4
                surface_change_x += 4
            return x,y,xi,yi,chestsp,exitsp,cx,cy,surface_change_x,surface_change_y,ex,ey
        x,y,xi,yi,chestsp,exitsp,cx,cy,surface_change_x,surface_change_y,ex,ey = player_spawn()
        
        running = False
        def check_collision(x, y):
            rect = pygame.Rect(x,y, 27,35)
            for wall in wallsg:
                if wall.rect.colliderect(rect):
                    return True
            return False
        def in_range(val1, val2, rn):
            return (val1 - rn) < val2 and (val1 + rn) > val2

        score_points = 0
        projs = []
        start_ticks = pygame.time.get_ticks()
        projectiles = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        for gen in generators:
            gen.new(enemies,Skelet_Pack())
        invulnerability = False
        invulnerability_time = 0.02
        invulnerability_time_ = 0
        harvest_time = 1
        harvest_time_ = 0
        attack_rate = 0.3
        algo_coldown = 6
        algo_time = 0
        isChestCollected = False
        last_algo = 0
        painted = bfs_search(int(xi/48), int(yi/48), enemies, cx, cy, surface, surface_change_x, surface_change_y)

        ENEMY_HIT_REWARD = -1
        CHEST_COLLECTION_REWARD = 200
        GENERATOR_DESTROY_REWARD = 10
        LOOSE_REWARD = -500
        ENEMY_KILL_REWARD = 5

        last_reward = 0

        def get_state():
            image = skimage.color.rgb2gray(pygame.surfarray.array3d(pygame.display.get_surface()))
            image = skimage.transform.resize(image, (10, 10))
            return np.array(image).flatten()

        state_old = get_state()
        next_action = agent.get_action(state_old)
        next_tile = SurfPart("empty.png", (x + next_action[0] * 48 - next_action[1] * 48),  (y + next_action[2] * 48 - next_action[3] * 48) )
        
        while run:
            clock.tick(200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            keys = pygame.key.get_pressed()
            notMoving = True
            if next_tile.rect.x < x :
                if check_collision(x - speed , y) == True:
                    notMoving = True
                else:
                    notMoving = False
                    for sur in surface:
                        sur.rect.x += speed
                    for wall in wallsg:
                        wall.rect.x += speed
                    for i in projectiles:
                        i.rect.x += speed
                    for en in enemies:
                        en.rect.x += speed
                    for gen in generators:
                        gen.rect.x += speed
                    surface_change_x += speed
                    next_tile.rect.x += speed
                    xi -= speed
                    turned_left = True
                    running = True
                    is_turned_x = True
                    is_turned_y = False
            if next_tile.rect.x > x:
                if check_collision(x + speed , y) == True:
                    notMoving = True
                else:
                    notMoving = False
                    for sur in surface:
                        sur.rect.x -= speed
                    for wall in wallsg:
                        wall.rect.x -= speed
                    for i in projectiles:
                        i.rect.x -= speed
                    for en in enemies:
                        en.rect.x -= speed
                    for gen in generators:
                        gen.rect.x -= speed
                    surface_change_x -= speed
                    next_tile.rect.x -= speed
                    xi += speed
                    turned_left = False
                    running = True
                    is_turned_x = True
                    is_turned_y = False
            if next_tile.rect.y > y:
                if check_collision(x , y + speed) == True:
                    notMoving = True
                else:
                    notMoving = False
                    for sur in surface:
                        sur.rect.y -= speed
                    for wall in wallsg:
                        wall.rect.y -= speed
                    for i in projectiles:
                        i.rect.y -= speed
                    for en in enemies:
                        en.rect.y -= speed
                    for gen in generators:
                        gen.rect.y -= speed
                    surface_change_y -= speed
                    next_tile.rect.y -= speed
                    yi += speed
                    running = True
                    turned_up = False
                    is_turned_x = False
                    is_turned_y = True
            if next_tile.rect.y < y:
                if check_collision(x , y - speed) == True:
                    notMoving = True
                else:
                    notMoving = False
                    for sur in surface:
                        sur.rect.y += speed
                    for wall in wallsg:
                        wall.rect.y += speed
                    for i in projectiles:
                        i.rect.y += speed
                    for en in enemies:
                        en.rect.y += speed
                    for gen in generators:
                        gen.rect.y += speed
                    next_tile.rect.y += speed
                    surface_change_y += speed
                    yi -= speed
                    running = True
                    is_turned_x = False
                    is_turned_y = True
            
            if (in_range(next_tile.rect.x, x, 12) and in_range(next_tile.rect.y, y, 12)) or check_collision(next_tile.rect.x, next_tile.rect.y) == True:
                state_new = get_state()
                if isChestCollected == False:
                    dis_to_target = ((ex - xi)**2 + (ey - yi)**2)**0.5
                else:
                    dis_to_target = ((cx - xi)**2 + (cy - yi)**2)**0.5
                last_reward += 80 - dis_to_target
                agent.train_short_memory(state_old, next_action, last_reward, state_new, False)
                agent.remember(state_old, next_action, last_reward, state_new, False)
                last_best_result += last_reward
                last_reward = 0
                state_old = state_new
                dis_to_target = 0
                
                next_action = agent.get_action(state_old)
                next_tile = SurfPart("empty.png", (x + next_action[0] * 48 - next_action[1] * 48),  (y + next_action[2] * 48 - next_action[3] * 48))

            rect = pygame.Rect(x,y, 27,39)
            if isChestCollected == False and chestsp.rect.colliderect(rect) == True:
                last_reward += CHEST_COLLECTION_REWARD
                isChestCollected = True
                algo_time = 0
                surface.remove(chestsp)

            if (pygame.time.get_ticks() - algo_time)/1000 >= algo_coldown and check_collision(x,y) == False:
                if len(painted.sprites()) != 0:
                    for pai in painted:
                        painted.remove(pai)
                        surface.remove(pai)
                start_time = datetime.now()
                painted = exec_algo(algos[current_search_algo],isChestCollected)
                    
                last_algo = datetime.now() - start_time
                algo_time = pygame.time.get_ticks()

            if (pygame.time.get_ticks() - start_ticks)/1000 >= attack_rate:
                dir = get_attack_direction(x, y, enemies, wallsg)
                if dir == -1:
                    pass
                else:
                    is_left = is_up = is_turned_x = is_turned_y = False
                    if dir == 0:
                        is_left = False
                        is_up = False
                        is_turned_x = True
                        is_turned_y = False
                    elif dir == 1:
                        is_left = True
                        is_up = False
                        is_turned_x = True
                        is_turned_y = False
                    elif dir == 2:
                        is_left = False
                        is_up = False
                        is_turned_x = False
                        is_turned_y = True
                    elif dir == 3:
                        is_left = False
                        is_up = True
                        is_turned_x = False
                        is_turned_y = True
                    projectiles.add(Projectile('Player/Attack/sword.png', x, y,
                    is_left,
                    is_up,
                    is_turned_x,
                    is_turned_y,
                    xi,
                    yi))
                    start_ticks = pygame.time.get_ticks()
            win.fill((0,0,0))
            if animCount + 2 >= 20:
                animCount = 0
            surface.draw(win)
            wallsg.draw(win)
            for i in projectiles:
                i.draw(win)
            if running == True:
                win.blit(pygame.transform.flip(player_walk[animCount // 6], turned_left, False), (x,y))
            else:
                win.blit(pygame.transform.flip(player_idle, turned_left, False), (x,y))
            for en in enemies:
                en.animate(win, xi, yi, surface_change_x, surface_change_y, projectiles)
            generators.draw(win)
            pygame.draw.rect(win, (0,0,0), pygame.Rect(620, 0, 280, 340))
            surfacegg = pygame.sprite.Group()
            win.blit(health,(640,50))
            win.blit(score,(780,50))
            win.blit(pclass,(695,10))
            win.blit(sp_left,(655,130))
            win.blit(alg,(655,220))
            scrope_points = font.render(str(score_points),True, (255,0,0))
            health_points_text = font.render(str(health_points),True, (255,0,0))
            spawners_text = font.render(str(generators_count),True, (255,0,0))
            last_algo_text = font.render(str(last_algo),True, (255,0,0))
            cur_algo_text = font.render(algos[current_search_algo],True, (255,0,0))
            win.blit(health_points_text,(780,90))
            win.blit(scrope_points,(640,90))
            win.blit(spawners_text,(730,170))
            win.blit(cur_algo_text,(720,260))
            win.blit(last_algo_text,(650,310))
            for gen in generators:
                for proj in projectiles:
                    if pygame.sprite.collide_rect(proj, gen) == True:
                        generators.remove(gen)
                        projectiles.remove(proj)
                        score_points += 50
                        last_reward += GENERATOR_DESTROY_REWARD
                        generators_count -= 1
                        break
                    if gen.check_if_killed(proj,projectiles) == True:
                        score_points += 5
                        continue
            
            for i in projectiles:
                if i.check_collission(wallsg,surfacegg):
                    projectiles.remove(i)
            for proj in projectiles:
                for en in enemies:
                    if pygame.sprite.collide_rect(proj, en) == True:
                        projectiles.remove(proj)
                        enemies.remove(en)
                        last_reward += ENEMY_KILL_REWARD
            for en in enemies:
                rect = pygame.Rect(x,y, 27,39)
                if en.rect.colliderect(rect) == True and invulnerability == False:
                    invulnerability = True
                    health_points -= 5
                    last_reward += ENEMY_HIT_REWARD
                    invulnerability_time_ = pygame.time.get_ticks()
                    break

            if isChestCollected == True and exitsp.rect.colliderect(rect) == True:
                run = False
                last_reward -= LOOSE_REWARD * 2
                state_new = agent.get_state()
                
                agent.train_short_memory(state_old, next_action, last_reward, state_new, True)
                agent.remember(state_old, next_action, last_reward, state_new, True)
                agent.n_games += 1
                agent.train_long_memory()

                if last_best_result > record:
                    record = last_best_result
                    agent.model.save()

            if (pygame.time.get_ticks() - invulnerability_time_)/1000 >= invulnerability_time:
                invulnerability = False
            if (pygame.time.get_ticks() - harvest_time_)/1000 >= harvest_time:
                health_points -= 1
                harvest_time_ = pygame.time.get_ticks()
            animCount += 1
            running = False
            for gen in generators:
                new_enemy = gen.spawn(wallsg)
                if new_enemy == None:
                    continue
                enemies.add(new_enemy)

            if health_points <= 0:
                run = False
                last_reward -= len(painted.sprites())
                last_reward += LOOSE_REWARD
                state_new = get_state()

                agent.train_short_memory(state_old, next_action, last_reward, state_new, True)
                agent.remember(state_old, next_action, last_reward, state_new, True)
                agent.n_games += 1
                agent.train_long_memory()

                if last_best_result > record:
                    record = last_best_result
                    agent.model.save()

            if generators_count == 0:
                run = False
                last_reward -= len(painted.sprites())
                last_reward -= LOOSE_REWARD
                state_new = get_state()
                
                agent.train_short_memory(state_old, next_action, last_reward, state_new, True)
                agent.remember(state_old, next_action, last_reward, state_new, True)
                agent.n_games += 1
                agent.train_long_memory()

                if last_best_result > record:
                    record = last_best_result
                    agent.model.save()

            pygame.display.update()

        games_count -= 1
        


def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
 
    return newText
 
# Colors
white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)
 
def main_menu():
    game()
 

main_menu()

pygame.quit()
