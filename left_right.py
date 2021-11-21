import Schieberegister as sr
import Gamepad
import numpy as np

#!/usr/bin/python3
# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = Gamepad.PS4()
print('Gamepad connected')

sr.init()
arr_l = np.zeros(8)
arr_r = np.zeros(8)
arr_l[:2] = 1
arr_r = np.roll(arr_l, -2)
sr.write_val(arr_l + arr_r)
print(arr_l + arr_r)
sr.show(1)

while 1:
    typ, button, value = gamepad.getNextEvent()
    
    if button == 'DPAD-X':
        arr_l = np.roll(arr_l, int(value))
        sr.write_val(arr_l + arr_r)
        print(arr_l + arr_r)
        
    if button in ['CIRCLE', 'SQUARE']:
        if button == 'SQUARE':
            value *= -1
        arr_r = np.roll(arr_r, int(value))
        sr.write_val(arr_l + arr_r)
        print(arr_l + arr_r)
    
    if button == 'PS' and value:
        break

sr.show(0)