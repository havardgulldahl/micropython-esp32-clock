# This is your main script.


print("Hello, world!")

import machine  # pylint: disable=import-error
import screen, networking, clock


def write_time(led):
    timestamp, time_explained = clock.now_human_repr()
    # screen.write_text(led, "{}:{}:{}".format(timestamp[3], timestamp[4], timestamp[5]))
    screen.write_text(led, time_explained)


led = screen.setup()
text = "Klokka til ODA"
screen.write_text(led, text)

tick = machine.Timer(0)
tick.init(period=1000, mode=tick.PERIODIC, callback=lambda x: write_time(led))
