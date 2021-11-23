#!/usr/bin/python3
import Schieberegister as sr
import Gamepad
import numpy as np
import time
import random

exit = 'PS'
x_dir = 'DPAD-X'
y_dir = 'DPAD-Y'

controller = Gamepad.PS4()
def new_game():
    global mat
    global pos_tuple
    mat = np.full((8,8), 1)
    pos_tuple = [(i, j) for i in range(8) for j in range(8)]

    global blink
    global direction
    global speed
    global snake
    global field
    global food
    global running
    global ingame

    blink = 0.3
    start = (0, 0)
    direction = (1, 0)
    speed = 0.5
    snake = [start]
    mat[snake[-1]] = 0
    field = pos_tuple
    field.remove(start)
    food = random.choice(field)
    mat[food] = 0
    running = 1
    ingame = 0

def move(direction):
    global snake
    global mat
    global field
    global food
    global speed
    head = snake[-1]
    snake.append((head[0] + direction[0],
                  head[1] + direction[1]))
    sh = snake[-1]
    if sh[0] not in range(8) or sh[1] not in range(8) or sh in snake[:-1]:
        field_blink()
        new_game()
        return
    mat[sh] = 0
    field.remove(snake[-1])
    if head != food:
        tail = snake.pop(0)
        mat[tail] = 1
        field.append(tail)
    else:
        speed *= 0.95
        mat[food] = 0
        food = random.choice(field)
        mat[food] = 0

def field_blink():
    global mat
    global food
    global snake
    if snake[-1] != food:
        mat[food] = 1
    time.sleep(0.1)
    for i in range(3):
        t = time.perf_counter()
        while time.perf_counter() - t < 0.2:
            sr.draw_frame(mat)
        time.sleep(0.2)

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = Gamepad.PS4()
print('Gamepad connected')

# define callback functions
def y_turn(plusminus):
    global direction
    global ingame
    if not ingame:
        ingame = 1
    if direction[1] and plusminus:
        direction = (int(plusminus), 0)
                 
def x_turn(plusminus):
    global direction
    global ingame
    if not ingame:
        ingame = 1
    if direction[0] and plusminus:
        direction = (0, int(plusminus))

def pause():
    global ingame
    ingame = 0

def end_of_game():
    global running
    if not ingame:
        running = 0
    else:
        pause()

# Start the background updating
controller.startBackgroundUpdates()

# Register callback functions
controller.addAxisMovedHandler('DPAD-X', x_turn)
controller.addAxisMovedHandler('DPAD-Y', y_turn)
controller.addButtonPressedHandler('PS', end_of_game)
controller.addButtonPressedHandler('CROSS', pause)

sr.init()
sr.show(1)
new_game()
t_frame = time.perf_counter()
t_food = t_frame

# Joystick events handled in the background
try:
    while running and controller.isConnected():
        
        sr.draw_frame(mat)
        
        if ingame:
            
            if time.perf_counter() - t_frame > speed:
                move(direction)
                t_frame = time.perf_counter()
                
            if time.perf_counter() - t_food > blink:
                if not food in snake:
                    mat[food] = 1 - mat[food]
                    t_food = time.perf_counter()
                 
finally:
    # Ensure the background thread is always terminated when we are done
    sr.show(0)
    gamepad.disconnect()
