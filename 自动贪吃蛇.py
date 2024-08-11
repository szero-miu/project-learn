import pygame
import random
import sys
from pygame.locals import *
from collections import deque

pygame.init()  # 初始化pygame库

# 窗口设置
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))  # 创建窗口
pygame.display.set_caption("简易贪吃蛇")  # 设置窗口标题

# 颜色设置
BLACK = (0, 0, 0)    # 黑色
WHITE = (255, 255, 255)  # 白色
GREEN = (0, 255, 0)  # 绿色（用于蛇的食物）
RED = (255, 0, 0)    # 红色（用于显示游戏结束信息）
BLUE = (0, 0, 255)   # 蓝色（用于绘制蛇）

# 蛇的设置
snake_block = 20     # 蛇块的大小（20x20像素）
snake_speed = 15     # 蛇的速度（每秒移动的帧数）
font_style = pygame.font.SysFont(None, 50)  # 字体设置，用于显示分数和游戏信息

def message(msg, color):
    """在屏幕上显示消息"""
    mesg = font_style.render(msg, True, color)  # 渲染消息
    win.blit(mesg, [WIDTH / 6, HEIGHT / 3])  # 在窗口上绘制消息

def draw_score(score):
    """在屏幕上显示分数"""
    value = font_style.render("Score: " + str(score), True, WHITE)  # 渲染分数
    win.blit(value, [0, 0])  # 在窗口的左上角绘制分数

def is_valid_position(x, y, snake_positions):
    """检查位置是否有效（即是否在屏幕内并且不在蛇身上）"""
    return (0 <= x < WIDTH) and (0 <= y < HEIGHT) and (x, y) not in snake_positions

def bfs(start, goal, snake_positions):
    """使用广度优先搜索（BFS）找到从起点到终点的路径"""
    directions = [(snake_block, 0), (0, snake_block), (-snake_block, 0), (0, -snake_block)]  # 可能的移动方向
    queue = deque([(start, [])])  # 初始化队列，包含起点和当前路径
    visited = set()  # 用于记录访问过的位置
    visited.add(start)
    
    while queue:
        (current, path) = queue.popleft()  # 从队列中取出当前点和路径
        
        if current == goal:  # 如果到达目标
            return path
        
        for direction in directions:
            new_x = current[0] + direction[0]  # 计算新的x坐标
            new_y = current[1] + direction[1]  # 计算新的y坐标
            new_position = (new_x, new_y)
            
            if is_valid_position(new_x, new_y, snake_positions) and new_position not in visited:
                visited.add(new_position)  # 记录访问的新位置
                queue.append((new_position, path + [direction]))  # 将新位置和路径添加到队列
    
    return []  # 如果没有路径返回空列表

def move_towards_food(x, y, foodx, foody, snake_List):
    """计算蛇朝向食物的移动方向"""
    snake_positions = set(tuple(segment) for segment in snake_List)  # 记录蛇身的所有位置
    path = bfs((x, y), (foodx, foody), snake_positions)  # 使用BFS找到从蛇头到食物的路径
    
    if path:
        next_direction = path[0]  # 返回路径中的第一个方向
        return next_direction
    else:
        return (0, 0)  # 如果没有路径，保持原地不动

def gameLoop():
    """游戏主循环"""
    game_over = False
    game_close = False

    # 初始化蛇的位置和速度
    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_List = []  # 存储蛇的身体
    Length_of_snake = 1
    score = 0  # 初始化分数

    # 初始化食物的位置
    foodx = round(random.randrange(0, WIDTH - snake_block) / 20.0) * 20.0
    foody = round(random.randrange(0, HEIGHT - snake_block) / 20.0) * 20.0

    while not game_over:
        while game_close:
            win.fill(BLACK)  # 填充背景为黑色
            message("Game Over! ", RED)  # 显示游戏结束消息
            draw_score(score)  # 显示分数
            pygame.display.update()  # 更新显示

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    quit()
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        pygame.quit()
                        quit()
                    if event.key == K_c:
                        gameLoop()  # 重新开始游戏

        # 自动移动逻辑
        x1_change, y1_change = move_towards_food(x1, y1, foodx, foody, snake_List)

        # 更新蛇的位置
        x1 += x1_change
        y1 += y1_change

        # 检测蛇是否碰到边界
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        # 绘制背景、食物和蛇
        win.fill(BLACK)
        pygame.draw.rect(win, GREEN, [foodx, foody, snake_block, snake_block])  # 绘制食物

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)  # 将新头部添加到蛇身
        if len(snake_List) > Length_of_snake:
            del snake_List[0]  # 移除蛇尾部以保持蛇的长度

        # 检测蛇是否咬到自己
        for segment in snake_List[:-1]:
            if segment == snake_Head:
                game_close = True

        # 绘制蛇的所有部分
        for segment in snake_List:
            pygame.draw.rect(win, BLUE, [segment[0], segment[1], snake_block, snake_block])

        draw_score(score)  # 显示分数
        pygame.display.update()  # 更新显示

        # 检查是否吃到食物
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, WIDTH - snake_block) / 20.0) * 20.0
            foody = round(random.randrange(0, HEIGHT - snake_block) / 20.0) * 20.0
            Length_of_snake += 1
            score += 10  # 每次吃到食物增加10分
            
            # 检查分数是否达到上限
            if score >= 1000:
                game_close = True

        # 控制游戏速度
        pygame.time.Clock().tick(snake_speed)

    pygame.quit()  # 退出pygame
    quit()

gameLoop()  # 启动游戏