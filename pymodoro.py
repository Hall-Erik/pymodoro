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
import thread
import os

sense = SenseHat()

# Times in minutes
work = 25
short_break = 5
long_break = 30

# Colors
white = [255]*3
red = [255] + [0]*2
green = [0,255,0]
light_green = [0,127,0]
light_red = [127] + [0]*2

# Marking colors
check = white
work_tick = green
break_tick = red
work_face = light_green
break_face = light_red

# Draw a check for each iteration completed.
def draw_checks(num):
    if num >= 1: sense.set_pixel(0,0,check)
    if num >= 2: sense.set_pixel(7,0,check)
    if num >= 3: sense.set_pixel(0,7,check)
    if num == 4: sense.set_pixel(7,7,check)

# Draw tick marks that go around the clock.
def draw_clock(pct, color):
    if pct >= 0: sense.set_pixel(4,2,color)
    if pct >= 1/12.0: sense.set_pixel(5,2,color)
    if pct >= 2/12.0: sense.set_pixel(5,3,color)
    if pct >= 3/12.0: sense.set_pixel(5,4,color)
    if pct >= 4/12.0: sense.set_pixel(5,5,color)
    if pct >= 5/12.0: sense.set_pixel(4,5,color)
    if pct >= 6/12.0: sense.set_pixel(3,5,color)
    if pct >= 7/12.0: sense.set_pixel(2,5,color)
    if pct >= 8/12.0: sense.set_pixel(2,4,color)
    if pct >= 9/12.0: sense.set_pixel(2,3,color)
    if pct >= 10/12.0: sense.set_pixel(2,2,color)
    if pct >= 11/12.0: sense.set_pixel(3,2,color)

def draw_clock_face(color):
    sense.set_pixel(3,3,color)
    sense.set_pixel(3,4,color)
    sense.set_pixel(4,3,color)
    sense.set_pixel(4,4,color)

# Runs the timer while updating ticks on the sensehat
def run_timer(duration, tick_color):
    start_time = datetime.now()
    while (datetime.now() - start_time) < timedelta(minutes=duration):
        minutes = (datetime.now() - start_time).seconds/60.0
        draw_clock(minutes/duration, tick_color)
        time.sleep(0.5) # no need to blast through this loop more than this.

# Exit on joystick action.
# Clears the screen, unless show_message is running
def joystick_listener():
    event = sense.stick.wait_for_event()
    sense.clear()
    os._exit(1)

try:
    thread.start_new_thread(joystick_listener, ())
except:
    print("Couldn't start thread.")
sense.low_light = True # normal mode is too bright for me.
sense.set_rotation(180) # the Pi is upside-down in my use case.

while True:
    sense.clear()
    checks = 0
    while checks < 4:
        sense.show_message(text_string="Work!", scroll_speed=0.05)
        draw_checks(checks)
        draw_clock_face(work_face)
        run_timer(work, work_tick)
        sense.show_message(text_string="Stop working!", scroll_speed=0.05)
        checks = checks + 1
        if checks == 4:
            sense.show_message(text_string="Take a long break.", scroll_speed=0.05)
            draw_checks(checks)
            draw_clock_face(break_face)
            run_timer(long_break, break_tick)
        else:
            sense.show_message(text_string="Take a short break.", scroll_speed=0.05)
            draw_checks(checks)
            draw_clock_face(break_face)
            run_timer(short_break, break_tick)
        # End while checks < 4
    # End while True
