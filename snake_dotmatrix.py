#!/usr/bin/python3
import Schieberegister as sr
import Gamepad
import numpy as np
import time
import random

controller = Gamepad.PS4()
running = 1
blink = 0.3
next_move = 1
moved = 0
buffer = [0, (0, 0)]

def new_game():
    global mat, pos_tuple, speed, snake, field, food, ingame, direction
    
    mat = np.full((8,8), 1)
    pos_tuple = [(i, j) for i in range(8) for j in range(8)]
    start = (0, 0)
    direction = (1, 1)
    speed = 0.3
    snake = [start]
    mat[snake[-1]] = 0
    field = pos_tuple
    field.remove(start)
    food = random.choice(field)
    mat[food] = 0
    ingame = 0

def move(direction):
    global snake, mat, field, food, speed
    
    head = snake[-1]
    snake.append((head[0] + direction[0],
                  head[1] + direction[1]))
    sh = snake[-1]
    if sh[0] not in range(8) or sh[1] not in range(8) or sh in snake[:-1]:
        if head != food:
            mat[food] = 1
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
        speed *= 0.97
        mat[food] = 0
        food = random.choice(field)
        mat[food] = 0

def field_blink():
    global mat
    
    time.sleep(0.1)
    for i in range(3):
        t = time.perf_counter()
        while time.perf_counter() - t < 0.2:
            sr.draw_frame(mat)
        time.sleep(0.1)

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = Gamepad.PS4()
print('Gamepad connected')

# define callback functions
def turn(axis_name, plusminus):
    global direction, ingame, next_move, buffer, moved
    
    if not ingame:
        ingame = 1
    if plusminus:
        if next_move:
            if axis_name[-1] == 'Y' and direction[1]:
                direction = (int(plusminus), 0)
            elif axis_name[-1] == 'X' and direction[0]:
                direction = (0, int(plusminus))
            next_move = 0
            moved = 1
        else:
            buffer[0] = 1
            if axis_name[-1] == 'Y':
                buffer[1] = (int(plusminus), 0)
            else:
                buffer[1] = (0, int(plusminus))
            
def pause():
    global ingame
    
    ingame = 1 - ingame

def end_of_game():
    global running
    
    if not ingame:
        running = 0
    else:
        pause()

# Start the background updating
controller.startBackgroundUpdates()

# Register callback functions
controller.addAxisMovedHandler('DPAD-X', turn)
controller.addAxisMovedHandler('DPAD-Y', turn)
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
                
            if time.perf_counter() - t_food > blink:
                if food not in snake:    
                    mat[food] = 1 - mat[food]
                    t_food = time.perf_counter()
            
            if time.perf_counter() - t_frame > speed:
                if buffer[0] and not moved:
                    direction = buffer[1]
                    buffer[0] = 0
                move(direction)
                next_move = 1
                moved = 0
                t_frame = time.perf_counter()
                 
finally:
    # Ensure the background thread is always terminated when we are done
    sr.show(0)
    gamepad.disconnect()
