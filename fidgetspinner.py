import pygame
from pygame import draw, event, display, time, font
from pygame import *
from math import *

pygame.init()

WIDTH = 500
HEIGHT = 500

screen = display.set_mode((WIDTH, HEIGHT))
clock = time.Clock()
display.set_caption("Fidget Spinner")

# Colors
background = (72, 0, 72)
white = (240, 240, 240)
red = (176, 58, 46)
dark_red = (120, 40, 31)
dark_gray = (23, 32, 42)
blue = (40, 116, 166)
dark_blue = (26, 82, 118)
yellow = (183, 149, 11)
dark_yellow = (125, 102, 8)
green = (29, 131, 72)
dark_green = (20, 90, 50)
orange = (230, 126, 34)
dark_orange = (126, 81, 9)


# Close the Pygame Window
def close():
    pygame.quit()
    exit()


# Drawing of Fidget Spinner on Pygame Window
def show_spinner(angle, col, dark_color):
    d = 80
    inner_d = 50
    x = WIDTH // 2 - d // 2
    y = HEIGHT // 2
    l = 200
    r = l // (3 ** 0.5)
    lw = 60

    # A little math for calculation the coordinates after rotation by some 'angle'
    # x = originx + r*cos(angle)
    # y = originy + r*sin(angle)

    centre = [x, y, d, d]
    centre_inner = [
        x + d // 2 - inner_d // 2,
        y + d // 2 - inner_d // 2,
        inner_d,
        inner_d,
    ]

    top = [x, y - l // 3 ** 0.5, d, d]
    top_inner = [x, y - l // 3 ** 0.5, inner_d, inner_d]

    top[0] = x + r * cos(radians(angle))
    top[1] = y + r * sin(radians(angle))
    top_inner[0] = x + d // 2 - inner_d // 2 + r * cos(radians(angle))
    top_inner[1] = y + d // 2 - inner_d // 2 + r * sin(radians(angle))

    left = [x - l // 2, y + l // (2 * 3 ** 0.5), d, d]
    left_inner = [x, y - l // 3 ** 0.5, inner_d, inner_d]

    left[0] = x + r * cos(radians(angle - 120))
    left[1] = y + r * sin(radians(angle - 120))
    left_inner[0] = x + d // 2 - inner_d // 2 + r * cos(radians(angle - 120))
    left_inner[1] = y + d // 2 - inner_d // 2 + r * sin(radians(angle - 120))

    right = [x + l // 2, y + l // (2 * 3 ** 0.5), d, d]
    right_inner = [x, y - l // 3 ** 0.5, inner_d, inner_d]

    right[0] = x + r * cos(radians(angle + 120))
    right[1] = y + r * sin(radians(angle + 120))
    right_inner[0] = x + d // 2 - inner_d // 2 + r * cos(radians(angle + 120))
    right_inner[1] = y + d // 2 - inner_d // 2 + r * sin(radians(angle + 120))

    # Drawing shapes on Pygame Window
    draw.line(
        screen,
        dark_color,
        (top[0] + d // 2, top[1] + d // 2),
        (centre[0] + d // 2, centre[1] + d // 2),
        lw,
    )
    draw.line(
        screen,
        dark_color,
        (left[0] + d // 2, left[1] + d // 2),
        (centre[0] + d // 2, centre[1] + d // 2),
        lw,
    )
    draw.line(
        screen,
        dark_color,
        (right[0] + d // 2, right[1] + d // 2),
        (centre[0] + d // 2, centre[1] + d // 2),
        lw,
    )
    draw.ellipse(screen, col, centre)
    draw.ellipse(screen, dark_color, centre_inner)
    draw.ellipse(screen, col, top)
    draw.ellipse(screen, dark_gray, top_inner, 10)
    draw.ellipse(screen, col, left)
    draw.ellipse(screen, dark_gray, left_inner, 10)
    draw.ellipse(screen, col, right)
    draw.ellipse(screen, dark_gray, right_inner, 10)


# Displaying Information on Pygame Window
def show_info():
    font_obj = font.Font(None, 22)
    text1 = font_obj.render("Click <-Left or Right -> to Spin ", True, white)
    text2 = font_obj.render("Click Space to change Color", True, white)
    screen.blit(text1, (15, 15))
    screen.blit(text2, (15, 45))


# The Main Function
def spinner():
    spin = True
    angle = 0
    speed = 0.0
    friction = 0.03
    right_pressed = False
    left_pressed = False

    direction = 1
    colors = [
        [red, dark_red],
        [blue, dark_blue],
        [yellow, dark_yellow],
        [green, dark_green],
        [orange, dark_orange],
    ]
    index = 0

    while spin:
        for ev in event.get():
            if ev.type == QUIT:
                close()
            if ev.type == KEYDOWN:
                if ev.key == K_RIGHT:
                    right_pressed = True
                    direction = 1
                if ev.key == K_LEFT:
                    left_pressed = True
                    direction = -1
                if ev.key == K_SPACE:
                    index += 1
                    if index >= len(colors):
                        index = 0
            if ev.type == KEYUP:
                left_pressed = False
                right_pressed = False

        # Changing the Angle of rotation
        if direction == 1:
            if right_pressed:	
                speed += 0.3
            else:
                speed -= friction
                if speed < 0:
                    speed = 0.0
        else:
            if left_pressed:
                speed -= 0.3
            else:
                speed += friction
                if speed > 0:
                    speed = 0.0

        screen.fill(background)
        angle += speed

        # Displaying Information and the Fidget Spinner
        show_spinner(angle, colors[index][0], colors[index][1])
        show_info()

        display.flip()
        clock.tick(90)


spinner()
