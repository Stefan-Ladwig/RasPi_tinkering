import Schieberegister as sr
import Gamepad
import numpy as np

# Wait for a connection
if not Gamepad.available():
    print('Please connect your gamepad...')
    while not Gamepad.available():
        time.sleep(1.0)
gamepad = Gamepad.PS4()
print('Gamepad connected')
