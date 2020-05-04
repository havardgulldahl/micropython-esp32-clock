"Main script"

print("main.py")

import machine  # pylint: disable=import-error
import screen, networking, clock, riddles


def write_time(led) -> None:
    timestamp, time_explained = clock.now_human_repr()
    screen.write_line(led, "{:02d}:{:02d}".format(timestamp[0], timestamp[1]), 1)
    screen.write_line(led, time_explained, 2)


def write_advice(led) -> None:
    adv = clock.get_advice()
    screen.write_line(led, adv, 3)


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

backlight_on = True


def handle_button(which, event):
    global backlight_on
    if which == "left":
        print("Left button")
        _new_bl = not backlight_on
        led.backlight(_new_bl)
        backlight_on = _new_bl
    else:
        print("Right button")


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
