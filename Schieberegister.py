#!/usr/bin/python3
import RPi.GPIO as GPIO
import numpy as np
import time

power = 21
give = 5
read = 6
write = 13
switch = 19
reset = 26

rewire = [4, 2, 5, 12, 7, 10, 9, 6,
          0, 15, 14, 1, 8, 3, 13, 11]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

def sigma(a):
    return [a[r] for r in rewire]

def init():
    GPIO.setup([give, read, write], GPIO.OUT, initial=0)
    GPIO.setup([switch, reset], GPIO.OUT, initial=1)
    GPIO.setup(power, GPIO.OUT, initial=1)

def on(l):
    if type(l) == list:
        for s in l:
            GPIO.output(s, 1)
    else:
        GPIO.output(l, 1)

def off(l):
    if type(l) == list:
        for s in l:
            GPIO.output(s, 0)
    else:
        GPIO.output(l, 0)

def write_val(values, commit=True):
    for v in reversed(sigma(values)):
        off([give, read])
        GPIO.output(give, bool(v))
        on(read)
    if commit:
        off(write)
        on(write)

def dot_matrix(mat, on_time=0.01):
    row = np.zeros(8)
    row[0] = 1
    for i in range(mat.shape[0]):
        write_val(mat[i, :], commit=0)
        write_val(row)
        time.sleep(on_time)

def draw_frame():        
        

def show(b):
    if not b:
        on(switch)
    else:
        off(switch)

