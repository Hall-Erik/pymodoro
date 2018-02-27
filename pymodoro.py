# coding: utf-8
'''
Pomodoro timer using the sense hat LED array

Typical pomodoro workflow:
1. Decide on the task to be done.
2. Set the pomodoro timer (traditionally to 25 minutes).
3. Work on the task.
4. End work when the timer rings and put a checkmark on a piece of paper.
5. If you have fewer than four checkmarks, take a short break (3–5 minutes), then go to step 2.
6. After four pomodoros, take a longer break (15-30 minutes), reset your checkmark count to zero, then go to step 1.
'''
from datetime import datetime, timedelta
from sense_hat import SenseHat
import time

sense = SenseHat()

# Times in minutes
work = 5
short_break = 5
long_break = 30

# Colors
white = [255]*3
red = [255] + [0]*2
green = [0,255,0]

# Marking colors
check = white
work_tick = green
break_tick = red

def draw_checks(num):
    if num >= 1: sense.set_pixel(0,0,check)
    if num >= 2: sense.set_pixel(7,0,check)
    if num >= 3: sense.set_pixel(0,7,check)
    if num == 4: sense.set_pixel(7,7,check)

def draw_clock(pct, color):
    if pct >= 1/12.0: sense.set_pixel(4,2,color)
    if pct >= 2/12.0: sense.set_pixel(5,2,color)
    if pct >= 3/12.0: sense.set_pixel(5,3,color)
    if pct >= 4/12.0: sense.set_pixel(5,4,color)
    if pct >= 5/12.0: sense.set_pixel(5,5,color)
    if pct >= 6/12.0: sense.set_pixel(4,5,color)
    if pct >= 7/12.0: sense.set_pixel(3,5,color)
    if pct >= 8/12.0: sense.set_pixel(2,5,color)
    if pct >= 9/12.0: sense.set_pixel(2,4,color)
    if pct >= 10/12.0: sense.set_pixel(2,3,color)
    if pct >= 11/12.0: sense.set_pixel(2,2,color)
    if pct >= 12/12.0: sense.set_pixel(3,2,color)

# TODO use joystick to quit
while True:
    sense.clear()
    checks = 0
    while checks < 4:
        sense.show_message(text_string="Work!")
        start_time = datetime.now()
        while (datetime.now() - start_time) < timedelta(minutes=work):
            # wait 25 mins updating clock
            minutes = (datetime.now() - start_time).seconds/60.0
            print(minutes)
            draw_clock(minutes/work, work_tick)
            time.sleep(0.5)

        sense.show_message(text_string="Stop working!")
        checks = checks + 1
        draw_checks(checks)
        if checks == 4:
            sense.show_message(text_string="Take a long break.")
            # wait 30 mins updating clock
        else:
            sense.show_message(text_string="Take a short break.")
            # wait 5 mins updating clock
        # End while checks < 4
    # End while True
