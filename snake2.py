import pygame
from pygame import time, display, event, draw, font, transform
from pygame.locals import *
from random import randint

FPS = 8
WIDTH = 640
HEIGHT = 480
CELLSIZE = 20
assert WIDTH % CELLSIZE == 0
assert HEIGHT % CELLSIZE == 0

CELLWIDTH = int(WIDTH / CELLSIZE)
CELLHEIGHT = int(HEIGHT / CELLSIZE)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

UP = "up"
DOWN = "down"
LEFT = "left"
RIGHT = "right"

HEAD = 0


def main():
    # noinspection PyGlobalUndefined
    global CLOCK, SCREEN, BASICFONT

    pygame.init()
    CLOCK = time.Clock()
    SCREEN = display.set_mode((WIDTH, HEIGHT))
    BASICFONT = font.Font("freesansbold.ttf", 18)
    display.set_caption("Wormy")

    show_start_screen()
    while True:
        run_game()
        show_game_over_screen()


def run_game():
    # set a random start point
    start_x = randint(5, CELLWIDTH - 6)
    start_y = randint(5, CELLHEIGHT - 6)
    worm_coords = [
        {"x": start_x, "y": start_y},
        {"x": start_x - 1, "y": start_y},
        {"x": start_x - 2, "y": start_y},
    ]
    direction = RIGHT

    # start the apple in a random place
    apple = get_random_location()

    # main game loop
    while True:
        for ev in event.get():  # event handling loop
            if ev.type == QUIT:
                terminate()
            elif ev.type == KEYDOWN:
                if (ev.key == K_LEFT or ev.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (ev.key == K_RIGHT or ev.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (ev.key in (K_UP, K_w)) and direction != DOWN:
                    direction = UP
                elif (ev.key in (K_DOWN, K_s)) and direction != UP:
                    direction = DOWN
                elif ev.key == K_ESCAPE:
                    terminate()

        # check if the worm hits itself or the edge
        if (
            worm_coords[HEAD]["x"] == -1
            or worm_coords[HEAD]["x"] == CELLWIDTH
            or worm_coords[HEAD]["y"] == -1
            or worm_coords[HEAD]["y"] == CELLHEIGHT
        ):
            return  # game over
        for worm_body in worm_coords[1:]:
            if (
                worm_body["x"] == worm_coords[HEAD]["x"]
                and worm_body["y"] == worm_coords[HEAD]["y"]
            ):
                return  # game over

        # check if the snake ate an apple
        if (
            worm_coords[HEAD]["x"] == apple["x"]
            and worm_coords[HEAD]["y"] == apple["y"]
        ):
            # don't remove the worm's tail segment
            # set a new apple elsewhere
            apple = get_random_location()
        else:
            # remove the worm's tail
            del worm_coords[-1]

        # move the worm, add/subtract a segment in the direction it is moving
        if direction == UP:
            new_head = {
                "x": worm_coords[HEAD]["x"],
                "y": worm_coords[HEAD]["y"] - 1,
                }
        elif direction == DOWN:
            new_head = {
                "x": worm_coords[HEAD]["x"],
                "y": worm_coords[HEAD]["y"] + 1,
                }
        elif direction == RIGHT:
            new_head = {
                "x": worm_coords[HEAD]["x"] + 1,
                "y": worm_coords[HEAD]["y"],
                }
        elif direction == LEFT:
            new_head = {
                "x": worm_coords[HEAD]["x"] - 1,
                "y": worm_coords[HEAD]["y"],
                }

        worm_coords.insert(0, new_head)
        SCREEN.fill(BGCOLOR)
        draw_grid()
        draw_worm(worm_coords)
        draw_apple(apple)
        draw_score(len(worm_coords) - 3)
        display.flip()
        CLOCK.tick(FPS)


def draw_press_key_msg():
    text = BASICFONT.render("press a key to play", True, DARKGRAY)
    text_rect = text.get_rect()
    text_rect.topleft = WIDTH - 200, HEIGHT - 30
    SCREEN.blit(text, text_rect)


def check_for_keypress():
    if len(event.get(QUIT)) > 0:
        terminate()

    keyup_events = event.get(KEYUP)
    if len(keyup_events) == 0:
        return None
    if keyup_events[0].key == K_ESCAPE:
        terminate()
    return keyup_events[0].key


def show_start_screen():
    title_font = font.Font(None, 100)
    text_1 = title_font.render("Wormy!", True, WHITE, DARKGREEN)
    text_2 = title_font.render("Wormy!", True, GREEN)

    deg_1 = 0
    deg_2 = 0

    while True:
        SCREEN.fill(BGCOLOR)

        rotate_text_1 = transform.rotate(text_1, deg_1)
        rotate_rect_1 = rotate_text_1.get_rect()
        rotate_rect_1.center = WIDTH // 2, HEIGHT // 2
        SCREEN.blit(rotate_text_1, rotate_rect_1)

        rotate_text_2 = transform.rotate(text_2, deg_2)
        rotate_rect_2 = rotate_text_2.get_rect()
        rotate_rect_2.center = WIDTH // 2, HEIGHT // 2
        SCREEN.blit(rotate_text_2, rotate_rect_2)

        draw_press_key_msg()

        if check_for_keypress():
            event.get()  # clears event queue
            return

        display.flip()
        CLOCK.tick(FPS)
        deg_1 += 3
        deg_2 += 7


def terminate():
    pygame.quit()
    exit()


def get_random_location():
    return {"x": randint(0, CELLWIDTH - 1), "y": randint(0, CELLHEIGHT - 1)}


def show_game_over_screen():
    game_over_font = font.Font("freesansbold.ttf", 150)
    game_text = game_over_font.render("Game", True, WHITE)
    over_text = game_over_font.render("Over", True, WHITE)
    game_rect = game_text.get_rect(midtop=(WIDTH / 2, 10))
    over_rect = over_text.get_rect(midtop=(WIDTH / 2, game_rect.height + 35))

    SCREEN.blit(game_text, game_rect)
    SCREEN.blit(over_text, over_rect)
    draw_press_key_msg()
    display.flip()
    time.wait(500)
    check_for_keypress()

    while True:
        if check_for_keypress():
            event.get()  # clear event queue
            return


def draw_score(score):
    score_text = BASICFONT.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(topleft=(WIDTH - 120, 10))
    SCREEN.blit(score_text, score_rect)


def draw_worm(coords):
    for i in coords:
        x = i["x"] * CELLSIZE
        y = i["y"] * CELLSIZE
        segment_rect = Rect(x, y, CELLSIZE, CELLSIZE)
        draw.rect(SCREEN, DARKGREEN, segment_rect)
        inner_segment_rect = Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        draw.rect(SCREEN, GREEN, inner_segment_rect)


def draw_apple(coord):
    x = coord["x"] * CELLSIZE
    y = coord["y"] * CELLSIZE
    apple_rect = Rect(x, y, CELLSIZE, CELLSIZE)
    draw.rect(SCREEN, RED, apple_rect)


def draw_grid():
    for x in range(0, WIDTH, CELLSIZE):
        draw.line(SCREEN, DARKGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELLSIZE):
        draw.line(SCREEN, DARKGRAY, (0, y), (WIDTH, y))


if __name__ == "__main__":
    main()
