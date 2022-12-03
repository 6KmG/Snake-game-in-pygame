import random
from pygame import *
import pygame
import time

init()
clock = pygame.time.Clock()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 480
BACKGROUND_COLOR = (50,50,50)
FPS = 300
DELAY = 0.25

class Snake:
    SIZE = 50
    STARTING_POINT = (100,100)
    COLOR = (0,0,255)
    pos_x = 0
    pos_y = 0
    movements = [False, False, None, True] # [0] is Upward, [1] is Downward, [2] is Left and [3] is Right (default)
    length = []
    SPEED = 3
    body = []

class Food:
    SIZE = 2
    COLOR = (255,255,0)
    POS = [random.randint(50,WINDOW_WIDTH-50),random.randint(50,WINDOW_HEIGHT-50)]

dt = (1000/FPS)/10
delay = 0.0
screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),RESIZABLE)
delay2 = time.time()+1
add = 0
ad = 0
score = 0

running = True
while running:
    display.set_caption(f"Snake game | FPS:{str(clock)[11:16]} | Score: {score}")
    if Snake.movements[0]:
        Snake.pos_y-=dt/720*screen.get_height()*Snake.SPEED
    if Snake.movements[1]:
        Snake.pos_y+=dt/720*screen.get_height()*Snake.SPEED
    if Snake.movements[2]:
        Snake.pos_x-=dt/1280*screen.get_width()*Snake.SPEED
    if Snake.movements[3]:
        Snake.pos_x+=dt/1280*screen.get_width()*Snake.SPEED

    Snake.length.append([Snake.pos_x,Snake.pos_y])

    for run in event.get():
        if run.type == KEYDOWN or run.type == KEYUP:

            if run.key == K_d and time.time() > delay and Snake.movements[3] != None:  #D
                delay = time.time()+DELAY
                Snake.movements = [False, False, None, True]

            elif run.key == K_a and time.time() > delay and Snake.movements[2] != None: #A
                delay = time.time()+DELAY
                Snake.movements = [False, False, True, None]

            elif run.key == K_w and time.time() > delay and Snake.movements[0] != None: #W
                delay = time.time()+DELAY
                Snake.movements = [True, None, False, False]

            elif run.key == K_s and time.time() > delay and Snake.movements[1] != None: #S
                delay = time.time()+DELAY
                Snake.movements = [None, True, False, False]
                    
        if run.type == QUIT:
            running = False

    screen.fill(BACKGROUND_COLOR)
    snake = draw.rect(screen, Snake.COLOR, [Snake.pos_x,Snake.pos_y,screen.get_width()/Snake.SIZE*9/5,screen.get_height()/Snake.SIZE*16/5])
    food = draw.circle(screen, Food.COLOR,Food.POS,(screen.get_height()+screen.get_width())/Food.SIZE*16/5/Snake.SIZE*9/5/5)
    
    if time.time() >= delay2:
        for i in range(len(Snake.length)-1,0,-4*round(FPS/24)):
            Snake.body.append(draw.rect(screen, Snake.COLOR, [Snake.length[i][0],Snake.length[i][1],screen.get_width()/Snake.SIZE*9/5,screen.get_height()/Snake.SIZE*16/5]))    
        
        for i in range(len(Snake.length)-8*round(FPS/24),0,-4*round(FPS/24)):
            if snake.centerx >= Snake.length[i][0] and snake.centerx <= Snake.length[i][0] + screen.get_width()/Snake.SIZE*9/5:
                if snake.centery >= Snake.length[i][1] and snake.centery <= Snake.length[i][1] + screen.get_height()/Snake.SIZE*16/5:
                    running = False

        if time.time() >= add:
            Snake.length.remove(Snake.length[0])

    if snake.center[0] <= food.bottomright[0] and snake.center[0] >= food.topleft[0] and time.time() >= delay2:
        if snake.center[1] <= food.bottomright[1] and snake.center[1] >= food.topleft[1]:
            Food.POS=[random.randint(50,screen.get_width()-50),random.randint(50,screen.get_height()-50)]
            add = time.time()+0.16
            ad+=12
            score += 1

    if snake.center[0]<=0 or snake.center[1]<=0 or snake.center[0]>=screen.get_width() or snake.center[1]>=screen.get_height():
        running = False

    display.update()
    clock.tick(FPS)
    
print(f"Your score: {score}")
