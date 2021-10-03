import pygame

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
    

