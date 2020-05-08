"Main script"

print("main.py")

import machine, gc  # pylint: disable=import-error
import screen, networking, clock, riddles

# import textwrap


def write_time(led) -> None:
    timestamp, time_explained = clock.now_human_repr()
    screen.write_line(led, "{:02d}:{:02d}".format(timestamp[0], timestamp[1]), 1)
    screen.write_line(led, time_explained, 2)
    screen.write_line(led, "", 3)  # blank
    screen.write_line(led, "", 0)  # blank


def write_advice(led) -> None:
    adv = clock.get_advice()
    screen.write_line(led, adv, 3)


def write_fullscreen(led, text: str) -> None:
    MAXCHARS = 16
    i = 0
    while len(text) > MAXCHARS:
        screen.write_line(led, text[:MAXCHARS], i)
        # print(text[:MAXCHARS])
        text = text[MAXCHARS:]
        i = i + 1
    screen.write_line(led, text, i)
    # print(text)
    for j in range(i + 1, 4):
        screen.write_line(led, "", j)  # blank


def state_clock_face(led) -> None:
    "Show the clock"
    write_time(led)
    write_advice(led)


led = screen.setup()
# TESTTEXT = b"D\xf8de bl\xe5b\xe6r"
# b'\xf8\xD8\xe6\xC6\xe5\xc5' = "øØæÆåÅ"
# screen.write_line(led, TESTTEXT, 3)


# start our clock
tick = machine.Timer(0)
tick.init(period=1000 * 60, mode=tick.PERIODIC, callback=lambda x: write_time(led))

# start advice machine
tock = machine.Timer(1)
tock.init(
    period=1000 * 60 * 30, mode=tick.PERIODIC, callback=lambda x: write_advice(led)
)

# constants
CLOCK = 1
QUESTION = 2
ANSWER = 3

# variables
backlight_on = True
screen_state = CLOCK
riddle = ()


def handle_button(which, event):
    global backlight_on, screen_state, riddle
    gc.collect()
    if which == "left":
        # print("Left button")
        _new_bl = not backlight_on
        led.backlight(_new_bl)
        backlight_on = _new_bl
    else:
        # print("Right button")
        # CLOCK -> QUESTION -> ANSWER
        if screen_state == CLOCK:
            # show question
            riddle = riddles.get_riddle()
            write_fullscreen(led, riddle[0])
            screen_state = QUESTION
        elif screen_state == QUESTION:
            # show answer
            write_fullscreen(led, riddle[1])
            riddle = ()
            screen_state = ANSWER
        else:
            # show clock
            state_clock_face(led)
            screen_state = CLOCK


# connect buttons=
pinL = machine.Pin(
    0,
    trigger=machine.Pin.IRQ_RISING,
    handler=lambda e: handle_button("left", e),
    debounce=500,
)
pinR = machine.Pin(
    35,
    trigger=machine.Pin.IRQ_RISING,
    handler=lambda e: handle_button("right", e),
    debounce=500,
)

# write clock face
state_clock_face(led)
