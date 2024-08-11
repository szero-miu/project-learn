import pygame
import random
import sys
from pygame.locals import *

pygame.init()

# 窗口设置
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("简易贪吃蛇")

# 颜色设置
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 蛇的设置
snake_block = 20
snake_speed = 15
font_style = pygame.font.SysFont(None, 50)

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    win.blit(mesg, [WIDTH / 6, HEIGHT / 3])

def draw_score(score):
    value = font_style.render("Score: " + str(score), True, WHITE)
    win.blit(value, [0, 0])

def gameLoop():
    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    score = 0

    foodx = round(random.randrange(0, WIDTH - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, HEIGHT - snake_block) / 20.0) * 20.0

    while not game_over:
        while game_close == True:
            win.fill(BLACK)
            message("you is a foolish", RED)
            draw_score(score)
            pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        win.fill(BLACK)
        pygame.draw.rect(win, GREEN, [foodx, foody, snake_block, snake_block])

        # 更新蛇的位置
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_close = True

        for segment in snake_List:
            pygame.draw.rect(win, BLUE, [segment[0], segment[1], snake_block, snake_block])

        draw_score(score)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, HEIGHT - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            score += 10  # 每次吃到食物增加10分

        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
