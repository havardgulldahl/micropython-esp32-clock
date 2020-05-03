"Main script"

print("Hello, world!")

import machine  # pylint: disable=import-error
import screen, networking, clock


def write_time(led):
    timestamp, time_explained = clock.now_human_repr()
    screen.write_line_two(led, "{:02d}:{:02d}".format(timestamp[0], timestamp[1]))
    screen.write_line_three(led, time_explained)


led = screen.setup()
# TESTTEXT = b"D\xf8de bl\xe5b\xe6r"
# b'\xf8\xD8\xe6\xC6\xe5\xc5' = "øØæÆåÅ"
# screen.write_line_four(led, TESTTEXT)


# start our clock
tick = machine.Timer(0)
tick.init(period=1000 * 60, mode=tick.PERIODIC, callback=lambda x: write_time(led))

# start
