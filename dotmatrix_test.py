#!/usr/bin/python3
import Schieberegister as sr
import Gamepad
import numpy as np
import time

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = Gamepad.PS4()
print('Gamepad connected')

sr.init()
mat = np.matrix(np.full((8, 8), 1))
mat[0,0] = 0
row = 0
zeros = np.zeros(16)
b = zeros
b[row] = 1
b[8:] = mat[row,:]
sr.write_val(b)
sr.show(1)

while 1:
    typ, button, value = gamepad.getNextEvent()
    
    if button == 'DPAD-X':
        mat = np.roll(mat, int(value), axis=1)
        b = np.zeros(16)
        b[row] = 1
        b[8:] = mat[row,:]
        sr.write_val(b)
    if button == 'DPAD-Y':
        mat = np.roll(mat, int(value), axis=0)
        row = (row + int(value)) % 8
        b = np.zeros(16)
        b[row] = 1
        b[8:] = mat[row,:]
        sr.write_val(b)
    
    if button == 'PS' and value:
        break

sr.show(0)