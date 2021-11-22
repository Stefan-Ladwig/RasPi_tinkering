import Schieberegister as sr
import Gamepad
import numpy as np
import time
import random

exit = 'PS'
x_dir = 'DPAD-X'
y_dir = 'DPAD-Y'

controller = Gamepad.PS4()

mat = np.full((8,8), 1)
pos_tuple = [(i, j) for i in range(8) for j in range(8)]

start = (0, 0)
direction = (1, 0)
speed = 2
snake = [start]
mat[snake[-1]] = 0
field = pos_tuple.remove(start)
food = random.choice(field_set)

def move(direction):
    head = snake[-1]
    snake.append((head[0] + direction[0],
                  head[1] + direction[1])
    mat[head] = 0
    field.remove(head)
    if head != food:
        tail = snake.pop(0)
        mat[tail] = 1
        field.append(tail)
    else:
        food = random.choice(field)

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = Gamepad.PS4()
print('Gamepad connected')

# Start the background updating
gamepad.startBackgroundUpdates()

# Joystick events handled in the background
try:
    while controller.isConnected():
        if gamepad.beenPressed(exit):
            print('EXIT')
            break

        if controller.axis(x_dir):
            
        if controller.axis(y_dir):


        time.sleep(1 / speed)
finally:
    # Ensure the background thread is always terminated when we are done
    gamepad.disconnect()
