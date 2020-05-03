# This is script that run when device boot up or wake from sleep.

# connect to board using
#  screen /dev/tty.usbserial-01EA7DE2 115200

import network, utime  # pylint: disable=import-error

from networking import wifi_up, telnet_up, mdns_up
from clock import ntp_sync

print("boot.py")


ntp_sync()

telnet_up()
mdns_up()
