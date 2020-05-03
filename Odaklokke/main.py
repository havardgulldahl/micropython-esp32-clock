# This is your main script.


print("Hello, world!")

import machine  # pylint: disable=import-error
import screen, networking, clock


def write_time(led):
    rtc = machine.RTC()
    # Return the current time as tuple: (year, month, day, hour, minute, second)
    timestamp = rtc.now()
    screen.write_text(led, "{}:{}:{}".format(timestamp[3], timestamp[4], timestamp[5]))


led = screen.setup()
text = "Klokka til ODA"
screen.write_text(led, text)

tick = machine.Timer(0)
tick.init(period=1000, mode=tick.PERIODIC, callback=lambda x: write_time(led))
