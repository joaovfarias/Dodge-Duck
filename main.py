import pygame
import os
import random
import sys
pygame.font.init()
pygame.mixer.init()

PROJECTILES_AMOUNT = 12
VELOCITY = 7


record = 0
FPS = 60
WIDTH, HEIGHT = 1050, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dodge Duck')

GREY = (137, 142, 140)
WHITE = (255, 255, 255)

POINTS_FONT = pygame.font.SysFont('comicsans', 40)
SCORE_FONT = pygame.font.SysFont('comicsans', 80)
RECORD_FONT = pygame.font.SysFont('comicsans', 45)

DUCK_HIT_BOOM = pygame.mixer.Sound(os.path.join("Assets", "boom.mp3"))
DUCK_HIT = pygame.mixer.Sound(os.path.join("Assets", "Duck Quack.mp3"))
PLAY_CLICK = pygame.mixer.Sound(os.path.join("Assets", "play_click.mp3"))

MAIN_MENU_TEXT = pygame.font.Font((os.path.join("Assets", "menufont.ttf")), 100)
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "background.png")), (WIDTH, HEIGHT))
CUTE_DUCK_WIDTH, CUTE_DUCK_HEIGTH = 50, 55
CUTE_DUCK = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'duck.png')), (CUTE_DUCK_WIDTH, CUTE_DUCK_HEIGTH))
KNIFE_WIDTH, KNIFE_HEIGHT = 65, 20


KNIVES = []
for i in range(PROJECTILES_AMOUNT):
    KNIFE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "knife.png")), (KNIFE_WIDTH, KNIFE_HEIGHT))
    KNIVES.append(KNIFE)


def main_menu():
    while True:
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()
        game_name = MAIN_MENU_TEXT.render("Dodge Duck", 1, (88, 238, 88))
        WIN.blit(BACKGROUND, (0, 0))
        WIN.blit(game_name, (260, 60))
        play_button_light = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "play_light.png")), (345, 125))
        play_button = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "play.png")), (340, 120))
        WIN.blit(play_button, ((WIDTH//2) - 165, HEIGHT//2 - 70))
        if play_button.get_rect(x=(WIDTH//2) - 165, y=HEIGHT//2 - 70).collidepoint(pygame.mouse.get_pos()):
            WIN.blit(play_button_light, (WIDTH//2 - 166, (HEIGHT//2 - 71)))
            if event.type == pygame.MOUSEBUTTONDOWN:
                PLAY_CLICK.play()
                main()
        pygame.display.update()


def draw_window(duck, projectiles, points, PROJECTILES_AMOUNT, hitbox):
    WIN.blit(BACKGROUND, (0, 0))
    WIN.blit(CUTE_DUCK, (duck.x, duck.y))
    POINTS_TEXT = POINTS_FONT.render("Score: " + str(points), 1, WHITE)
    WIN.blit(POINTS_TEXT, (790, 5))
    for i in range(PROJECTILES_AMOUNT):
        WIN.blit(KNIVES[i], (projectiles[i].x, projectiles[i].y))
    pygame.display.update() 
     

def duck_movement(duck, hitbox):
    keys_pressed = pygame.key.get_pressed()
    if (keys_pressed[pygame.K_a] or keys_pressed[pygame.K_LEFT]) and duck.x > 0:
        duck.x -= VELOCITY
        hitbox.x -= VELOCITY
    if (keys_pressed[pygame.K_d] or keys_pressed[pygame.K_RIGHT]) and duck.x < 990:
        duck.x += VELOCITY
        hitbox.x += VELOCITY
    if (keys_pressed[pygame.K_w] or keys_pressed[pygame.K_UP]) and duck.y > 5:
        duck.y -= VELOCITY
        hitbox.y -= VELOCITY
    if (keys_pressed[pygame.K_s] or keys_pressed[pygame.K_DOWN]) and duck.y < 400:
        duck.y += VELOCITY
        hitbox.y += VELOCITY


def draw_max_points(text, record):
    WIN.blit(BACKGROUND, (0, 0))
    drawtext = SCORE_FONT.render(text, 1, WHITE)
    drawrecord = RECORD_FONT.render(record, 1, WHITE)
    WIN.blit(drawtext, (WIDTH//2 - drawtext.get_width()//2, (HEIGHT//2 - drawtext.get_width()//2) + 50))
    WIN.blit(drawrecord, (WIDTH//2 - drawtext.get_width()//2 + 60, (HEIGHT//2 - drawtext.get_width()//2) + 145))
    pygame.display.update()
    pygame.time.delay(1500)


def main():
    KNIFE_VELOCITY = 10
    global record
    projectiles = []
    knife_distance = 170
    points = 0
    hitbox = pygame.Rect(935, 261, CUTE_DUCK_WIDTH - 20, CUTE_DUCK_HEIGTH - 17)
    duck = pygame.Rect(925, 250, CUTE_DUCK_WIDTH, CUTE_DUCK_HEIGTH)

    for i in range(PROJECTILES_AMOUNT):
        projectile = pygame.Rect(-90 - knife_distance, random.randint(5, 430), KNIFE_WIDTH, KNIFE_HEIGHT)
        projectiles.append(projectile)
        knife_distance += 170

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():    
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

        draw_window(duck, projectiles, points, PROJECTILES_AMOUNT, hitbox)
        duck_movement(duck, hitbox)
        for i in range(PROJECTILES_AMOUNT):
            projectiles[i].x += KNIFE_VELOCITY
            if projectiles[i].x > 1300:
                points += 1
                KNIFE_VELOCITY += 0.02
                projectiles[i] = pygame.Rect(-90, random.randint(5, 430), KNIFE_WIDTH, KNIFE_HEIGHT)
            if projectiles[i].colliderect(hitbox):
                if points < 100:
                    DUCK_HIT.play()
                else:
                    DUCK_HIT_BOOM.play()
                if points > record:
                    record = points
                draw_max_points(f"Score: {points}", f"Record: {record}")
                main()
  

if __name__ == '__main__':
    main_menu()