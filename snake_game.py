import random
from pygame import *
import pygame
import time
import tkinter.messagebox

init()
clock = pygame.time.Clock()

WINDOW_WIDTH, WINDOW_HEIGHT = 800, 480
BACKGROUND_COLOR = (65,126,176)
FPS = 77
DELAY = 0.25

class Snake:
    SIZE = 50
    STARTING_POINT = (100,100)
    COLOR = (255,232,115)
    pos_x = 0
    pos_y = 0
    movements = [False, False, None, True] # [0] is Upward, [1] is Downward, [2] is Left and [3] is Right (default)
    length = []
    SPEED = 6
    body = []

class Food:
    SIZE = 2
    COLOR = (255,255,255)
    POS = [random.randint(50,WINDOW_WIDTH-50),random.randint(50,WINDOW_HEIGHT-50)]

dt = (1000/FPS)/10
cooldown = 0.0
screen = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),RESIZABLE)
delay2 = time.time()+1
add = 0
ad = 0
score = 0

running = True
while running:
    display.set_caption(f"Snake game | FPS:{str(clock)[11:16]} | Score: {score}")

    # Movements

    if Snake.movements[0]:
        Snake.pos_y-=dt/720*screen.get_height()*Snake.SPEED
    if Snake.movements[1]:
        Snake.pos_y+=dt/720*screen.get_height()*Snake.SPEED
    if Snake.movements[2]:
        Snake.pos_x-=dt/1280*screen.get_width()*Snake.SPEED
    if Snake.movements[3]:
        Snake.pos_x+=dt/1280*screen.get_width()*Snake.SPEED

    # Adding the tiles

    Snake.length.append([Snake.pos_x,Snake.pos_y])

    # Keys

    for run in event.get():
        if run.type == KEYDOWN:

            if run.key == K_d and time.time() > cooldown and Snake.movements[3] != None:  #Key "D"
                cooldown = time.time()+DELAY
                Snake.movements = [False, False, None, True]

            elif run.key == K_a and time.time() > cooldown and Snake.movements[2] != None: #Key "A"
                cooldown = time.time()+DELAY
                Snake.movements = [False, False, True, None]

            elif run.key == K_w and time.time() > cooldown and Snake.movements[0] != None: #Key "W"
                cooldown = time.time()+DELAY
                Snake.movements = [True, None, False, False]

            elif run.key == K_s and time.time() > cooldown and Snake.movements[1] != None: #Key "S"
                cooldown = time.time()+DELAY
                Snake.movements = [None, True, False, False]

        # Quit on exit button

        if run.type == QUIT:
            running = False

    # Draw stuff to the screen

    screen.fill(BACKGROUND_COLOR)
    snake = draw.rect(screen, Snake.COLOR, [Snake.pos_x,Snake.pos_y,screen.get_width()/Snake.SIZE*9/5,screen.get_height()/Snake.SIZE*16/5])
    food = draw.circle(screen, Food.COLOR,Food.POS,(screen.get_height()+screen.get_width())/Food.SIZE*16/5/Snake.SIZE*9/5/5)
    
    if time.time() >= delay2:   
        for i in range(len(Snake.length)-1,0,int(-(13/Snake.SPEED)*(FPS/24))):
            Snake.body.append(draw.rect(screen, Snake.COLOR, [Snake.length[i][0],Snake.length[i][1],screen.get_width()/Snake.SIZE*9/5,screen.get_height()/Snake.SIZE*16/5]))    
        
        # Exit on touching the tail
        for i in range(int(len(Snake.length)-8*(FPS/24)),0,int(-(13/Snake.SPEED)*(FPS/24))):
            if snake.centerx >= Snake.length[i][0] and snake.centerx <= Snake.length[i][0] + screen.get_width()/Snake.SIZE*9/5:
                if snake.centery >= Snake.length[i][1] and snake.centery <= Snake.length[i][1] + screen.get_height()/Snake.SIZE*16/5:
                    running = False

        # Remove the previous tiles, thus make the illusion that the snake is moving

        if time.time() >= add:
            Snake.length.remove(Snake.length[0])

    # Food position and behaviour

    if snake.center[0] <= food.bottomright[0]+10 and snake.center[0] >= food.topleft[0]-10 and time.time() >= delay2:
        if snake.center[1] <= food.bottomright[1]+10 and snake.center[1] >= food.topleft[1]-10:
            Food.POS=[random.randint(50,screen.get_width()-50),random.randint(50,screen.get_height()-50)]
            add = time.time()+0.16
            ad+=12
            score += 1

    # Quit on Snake leaves the screen

    if snake.center[0]<=0 or snake.center[1]<=0 or snake.center[0]>=screen.get_width() or snake.center[1]>=screen.get_height():
        running = False

    display.update()
    clock.tick(FPS)

tkinter.messagebox.showinfo("Score",f"Your score: {score}")
