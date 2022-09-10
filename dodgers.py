import pygame
from pygame import event, time, display, mouse, font, mixer, image, transform
from pygame.locals import *
from random import randint

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
FPS = 30
MINSIZE = 10
MAXSIZE = 25
MINSPEED = 1
MAXSPEED = 8
ADDNEWRATE = 8
PLAYERMOVERATE = 5


def terminate():
    pygame.quit()
    exit()


def wait_for_player_key():
    while True:
        for ev in event.get():
            if ev.type == QUIT:
                terminate()
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    terminate()
                return


def player_has_hit(p_rect, enemy_list):
    for enemy in enemy_list:
        if p_rect.colliderect(enemy["rect"]):
            return True
    return False


def draw_text(text, fontobj, surface, x, y):
    text_obj = fontobj.render(text, True, TEXTCOLOR)
    text_obj_rect = text_obj.get_rect(topleft=(x, y))
    surface.blit(text_obj, text_obj_rect)


pygame.init()
clock = time.Clock()
screen = display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
display.set_caption("Dodgers")
mouse.set_visible(False)

font1 = font.Font(None, 48)
game_over_sound = mixer.Sound("./Image Files/gameover.wav")
mixer.music.load("./Image Files/background.mid")

player_image = image.load("./Image Files/player.png")
player_rect = player_image.get_rect()
enemy_image = image.load("./Image Files/baddie.png")

screen.fill(BG_COLOR)
draw_text("Press any key to start", font1, screen, WINDOWWIDTH / 3, WINDOWHEIGHT / 3)
display.flip()
wait_for_player_key()
top_score = 0
while True:
    enemies = []
    score = 0
    player_rect.topleft = (WINDOWWIDTH / 2, WINDOWHEIGHT - 50)
    move_left = move_right = move_up = move_down = False
    reverse_cheat = slow_cheat = False
    enemy_add_counter = 0
    mixer.music.play(-1, 0.0)

    while True:
        score += 1
        for ev in event.get():
            if ev.type == QUIT:
                terminate()
            
            if ev.type == KEYDOWN:
                if ev.key == K_z:
                    reverse_cheat = True
                if ev.key == K_x:
                    slow_cheat = True
                if ev.key == K_LEFT or ev.key == K_a:
                    move_right = False
                    move_left = True
                if ev.key == K_RIGHT or ev.key == K_d:
                    move_right = True
                    move_left = False
                if ev.key in (K_UP, K_w):
                    move_down = False
                    move_up = True
                if ev.key in (K_DOWN, K_s):
                    move_down = True
                    move_up = False

            if ev.type == KEYUP:
                if ev.key == K_z:
                    reverse_cheat = False
                    score = 0
                if ev.key == K_x:
                    slow_cheat = False
                    score = 0
                if ev.key == K_ESCAPE:
                    terminate()
                if ev.key == K_LEFT or ev.key == K_a:
                    move_left = False
                if ev.key == K_RIGHT or ev.key == K_d:
                    move_right = False
                if ev.key == K_UP or ev.key == K_w:
                    move_up = False
                if ev.key == K_DOWN or ev.key == K_s:
                    move_down = False
            
            if ev.type == MOUSEMOTION:
                player_rect.centerx = ev.pos[0]
                player_rect.centery = ev.pos[1]

        if not reverse_cheat and not slow_cheat:
            enemy_add_counter += 1
        if enemy_add_counter == ADDNEWRATE:
            enemy_add_counter = 0
            enemy_size = randint(MINSIZE, MAXSIZE)
            new_enemy = {
                "rect": pygame.Rect(
                    randint(0, WINDOWWIDTH - enemy_size),
                    0 - enemy_size,
                    enemy_size,
                    enemy_size,
                ),
                "speed": randint(MINSPEED, MAXSPEED),
                "surface": transform.scale(enemy_image, (enemy_size, enemy_size)),
            }
            enemies.append(new_enemy)

        # move the baddie around
        if move_left and player_rect.left > 0:
            player_rect.move_ip(-1 * PLAYERMOVERATE, 0)
        if move_right and player_rect.right < WINDOWWIDTH:
            player_rect.move_ip(PLAYERMOVERATE, 0)
        if move_up and player_rect.top > 0:
            player_rect.move_ip(0, -1 * PLAYERMOVERATE)
        if move_down and player_rect.bottom < WINDOWHEIGHT:
            player_rect.move_ip(0, PLAYERMOVERATE)

        # move the baddies down
        for b in enemies:
            if not reverse_cheat and not slow_cheat:
                b["rect"].move_ip(0, b["speed"])
            elif reverse_cheat:
                b["rect"].move_ip(0, -5)
            elif slow_cheat:
                b["rect"].move_ip(0, 1)
            # delete baddies that are beyond the screen
            if b["rect"].top > WINDOWHEIGHT:
                enemies.remove(b)

        # draw the game background
        screen.fill(BG_COLOR)

        # draw current score and top score
        draw_text(f"Score: {score}", font1, screen, 10, 0)
        draw_text(f"Top Score: {top_score}", font1, screen, 10, 40)

        # draw the player
        screen.blit(player_image, player_rect)

        # draw each baddie
        for b in enemies:
            screen.blit(b["surface"], b["rect"])

        display.flip()

        # check if any baddie has hit th player
        if player_has_hit(player_rect, enemies):
            if score > top_score:
                top_score = score
            break

        clock.tick(FPS)

    mixer.music.stop()
    game_over_sound.play()
    draw_text("GAME OVER", font1, screen, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    draw_text(
        "Press any key to play again",
        font1,
        screen,
        (WINDOWWIDTH / 3) - 80,
        (WINDOWHEIGHT / 3) + 50,
    )
    display.flip()
    wait_for_player_key()
    game_over_sound.stop()
