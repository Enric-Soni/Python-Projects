import pygame
from random import randint
from pygame import Surface, draw, event, display, sprite, time, font
from pygame.locals import *

# colors
BG_COLOR = (0, 0, 0)
PADDLE_COLOR = (255, 255, 255)
BALL_COLOR = (255, 255, 255)
FPS = 50

pygame.init()
screen = display.set_mode((600, 600))
screen_rect = screen.get_rect()
display.set_caption("Pong!")
clock = time.Clock()
pygame.key.set_repeat(1, 40)

font1 = font.Font(None, 48)
score_1 = 0
score_2 = 0


class Paddle(sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.color = color
        self.width = width
        self.height = height
        self.image = Surface([self.width, self.height])
        draw.rect(self.image, self.color, (0, 0, self.width, self.height))
        self.rect = self.image.get_rect()

    def move_down(self):
        self.rect.y = self.rect.y + 10
        if self.rect.y >= 500:
            self.rect.y = 500

    def move_up(self):
        self.rect.y = self.rect.y - 10
        if self.rect.y <= 0:
            self.rect.y = 0


class Ball(sprite.Sprite):
    def __init__(self, color, size):
        super().__init__()
        self.color = color
        self.size = size
        self.image = Surface([self.size * 2, self.size * 2])
        draw.circle(self.image, self.color, (size, size), size)
        self.rect = self.image.get_rect()
        if randint(0, 1) == 0:
            x_vel = randint(5, 10)
        else:
            x_vel = randint(-10, -5)
        y_vel = randint(-5, 5)
        self.velocity = [x_vel, y_vel]

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


paddleA = Paddle(PADDLE_COLOR, 10, 100)
paddleA.rect.x = 10
paddleA.rect.centery = 200

paddleB = Paddle(PADDLE_COLOR, 10, 100)
paddleB.rect.x = 580
paddleB.rect.centery = 200

ball = Ball(BALL_COLOR, 7)
ball.rect.center = (300, 300)

sprite_list = sprite.Group()
sprite_list.add(paddleA)
sprite_list.add(paddleB)
sprite_list.add(ball)


while True:
    for ev in event.get():
        if ev.type == QUIT:
            pygame.quit()
            exit()
        if ev.type == KEYDOWN:
            if ev.key == K_DOWN:
                paddleB.move_down()
            if ev.key == K_UP:
                paddleB.move_up()
            if ev.key == K_w:
                paddleA.move_up()
            if ev.key == K_s:
                paddleA.move_down()

    if ball.rect.left <= screen_rect.left:
        ball.velocity[0] = -ball.velocity[0]
        score_2 += 1
    if ball.rect.right >= screen_rect.right:
        ball.velocity[0] = -ball.velocity[0]
        score_1 += 1
    if ball.rect.bottom >= screen_rect.bottom:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.top <= screen_rect.top:
        ball.velocity[1] = -ball.velocity[1]

    if sprite.collide_mask(ball, paddleA) or sprite.collide_mask(ball, paddleB):
        ball.velocity[0] = -ball.velocity[0]
        ball.velocity[1] = randint(-5, 5)

    score1_text = font1.render(str(score_1), True, PADDLE_COLOR)
    score2_text = font1.render(str(score_2), True, PADDLE_COLOR)

    score1_rect = score1_text.get_rect(center=(20, 20))
    score2_rect = score2_text.get_rect(center=(580, 21))

    screen.fill(BG_COLOR)

    sprite_list.update()
    sprite_list.draw(screen)

    screen.blit(score1_text, score1_rect)
    screen.blit(score2_text, score2_rect)

    display.flip()
    clock.tick(FPS)