import pygame, sys
import pygame_menu
from player_stuff import *
from level_generator import surface,lvl_matrix,wallsg,generators,spawn_spawners,re_gen,spawn_chest,spawn_exit
import numpy as np
from enemy import *
from path_searcher import *



pygame.init()
win_width = 900
win_height = 700
clock = pygame.time.Clock()
win = pygame.display.set_mode((win_width, win_width))

pygame.display.set_caption("Gauntlet_Reforged")
 

def game():
    re_gen()
    font = pygame.font.Font("Fonts\EightBitDragon.ttf", 24)
    score = font.render("Health",True, (255,0,0))
    health = font.render("Score",True, (255,0,0))
    pclass = font.render("Warrior",True, (255,0,0))
    sp_left = font.render("Spawners left",True, (255,0,0))
    alg = font.render("Current algo",True,(255,0,0))
    param_rect = pygame.Rect(610,0, 140,140)
    x = 800
    y = 700
    width = 32
    height = 32
    speed = 5
    health_points = 5000

    run = True
    turned_left = False
    turned_up = False
    is_turned_x = True
    is_turned_y = True
    animCount = 0
    generators_count = 10
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
    def exec_algo(algo):
        if algo == "bfs":
            c_gr = bfs_search(int(xi/48),int(yi/48),enemies,cx,cy,surface,surface_change_x,surface_change_y)
            e_gr = bfs_search(int(xi/48),int(yi/48),enemies,ex,ey,surface,surface_change_x,surface_change_y)
            e_gr.add(c_gr.sprites())
            c_gr.empty()
            return e_gr
        elif algo == "dfs":
            c_gr = dfs_search(int(xi/48),int(yi/48),enemies,cx,cy,surface,surface_change_x,surface_change_y)
            e_gr = dfs_search(int(xi/48),int(yi/48),enemies,ex,ey,surface,surface_change_x,surface_change_y)
            e_gr.add(c_gr.sprites())
            c_gr.empty()
            return e_gr
        elif algo == "uniform":
            c_gr = uniform_cost_search(int(xi/48),int(yi/48),enemies,cx,cy,surface,surface_change_x,surface_change_y)
            e_gr = uniform_cost_search(int(xi/48),int(yi/48),enemies,ex,ey,surface,surface_change_x,surface_change_y)
            e_gr.add(c_gr.sprites())
            c_gr.empty()
            return e_gr

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
        rect = pygame.Rect(x,y, 27,39)
        for wall in wallsg:
            if wall.rect.colliderect(rect):
                return True
        return False

    score_points = 0
    projs = []
    start_ticks = pygame.time.get_ticks()
    projectiles = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    painted = uniform_cost_search(int(xi/48),int(yi/48),enemies,cx,cy,surface,surface_change_x,surface_change_y)
    for gen in generators:
        gen.new(enemies,Skelet_Pack())
    invulnerability = False
    invulnerability_time = 0.2
    invulnerability_time_ = 0
    harvest_time = 1
    harvest_time_ = 0
    attack_rate = 0.3
    algo_coldown = 0.1
    algo_time = 0
    isChestCollected = False
    
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if check_collision(x - speed/20 - speed, y) == True:
                turned_left = True
            else:
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
                xi -= speed
                turned_left = True
                running = True
                is_turned_x = True
                is_turned_y = False
        if keys[pygame.K_RIGHT]:
            if check_collision(x + speed , y) == True:
                turned_left = False
            else:
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
                xi += speed
                turned_left = False
                running = True
                is_turned_x = True
                is_turned_y = False
        if keys[pygame.K_DOWN]:
            if check_collision(x , y + speed) == True:
                turned_left = False
            else:
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
                yi += speed
                running = True
                turned_up = False
                is_turned_x = False
                is_turned_y = True
        if keys[pygame.K_UP]:
            if check_collision(x , y - speed) == True:
                turned_left = False
            else:
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
                surface_change_y += speed
                yi -= speed
                running = True
                turned_up = True
                is_turned_x = False
                is_turned_y = True
        if keys[pygame.K_z]:
            if (pygame.time.get_ticks() - algo_time)/1000 >= algo_coldown:
                current_search_algo = change_algo(current_search_algo)
                algo_time = pygame.time.get_ticks()
        if keys[pygame.K_x]:
            if (pygame.time.get_ticks() - algo_time)/1000 >= algo_coldown:
                if len(painted.sprites()) != 0:
                    for pai in painted:
                        painted.remove(pai)
                        surface.remove(pai)
                painted = exec_algo(algos[current_search_algo])
                algo_time = pygame.time.get_ticks()
        if keys[pygame.K_SPACE]:
            if (pygame.time.get_ticks() - start_ticks)/1000 >= attack_rate:
                projectiles.add(Projectile('Player/Attack/sword.png',x,y,turned_left,turned_up,is_turned_x,is_turned_y))
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
            en.animate(win,x,y)
        generators.draw(win)
        pygame.draw.rect(win, (0,0,0), pygame.Rect(620, 0, 280, 300))
        surfacegg = pygame.sprite.Group()
        win.blit(health,(640,50))
        win.blit(score,(780,50))
        win.blit(pclass,(695,10))
        win.blit(sp_left,(655,130))
        win.blit(alg,(655,220))
        scrope_points = font.render(str(score_points),True, (255,0,0))
        health_points_text = font.render(str(health_points),True, (255,0,0))
        spawners_text = font.render(str(generators_count),True, (255,0,0))
        cur_algo_text = font.render(algos[current_search_algo],True, (255,0,0))
        win.blit(health_points_text,(780,90))
        win.blit(scrope_points,(640,90))
        win.blit(spawners_text,(730,170))
        win.blit(cur_algo_text,(720,260))
        for gen in generators:
            for proj in projectiles:
                if pygame.sprite.collide_rect(proj, gen) == True:
                    generators.remove(gen)
                    projectiles.remove(proj)
                    score_points += 50
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
        for en in enemies:
            rect = pygame.Rect(x,y, 27,39)
            if en.rect.colliderect(rect) == True and invulnerability == False:
                invulnerability = True
                health_points -= 5
                invulnerability_time_ = pygame.time.get_ticks()
                break

        rect = pygame.Rect(x,y, 27,39)
        if isChestCollected == False and chestsp.rect.colliderect(rect) == True:
            isChestCollected = True
            surface.remove(chestsp)

        if isChestCollected == True and exitsp.rect.colliderect(rect) == True:
            run = False

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
        if generators_count == 0:
            run = False
        pygame.display.update()


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
    font = "Fonts\EightBitDragon.ttf"
    menu=True
    selected="start"
 
    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    selected="start"
                elif event.key==pygame.K_DOWN:
                    selected="quit"
                if event.key==pygame.K_RETURN:
                    if selected =="start":
                        game()
                        lvl_matrix = np.ones((50,50))
                        generators.empty()
                        surface.empty()
                        wallsg.empty()
                    if selected=="quit":
                        pygame.quit()
                        quit()
 
        # Main Menu UI
        win.fill(black)
        title= text_format("+- Gauntlet", font, 70, yellow)
        if selected=="start":
            text_start=text_format("START", font, 55, red)
        else:
            text_start = text_format("START", font, 55, white)
        if selected=="quit":
            text_quit=text_format("QUIT", font, 55, red)
        else:
            text_quit = text_format("QUIT", font, 55, white)
 
        title_rect=title.get_rect()
        start_rect=text_start.get_rect()
        quit_rect=text_quit.get_rect()
 
        # Main Menu Text
        win.blit(title, (win_width/2 - (title_rect[2]/2), 80))
        win.blit(text_start, (win_width/2 - (start_rect[2]/2), 300))
        win.blit(text_quit, (win_width/2 - (quit_rect[2]/2), 430))
        pygame.display.update()
        clock.tick(30)

main_menu()

pygame.quit()