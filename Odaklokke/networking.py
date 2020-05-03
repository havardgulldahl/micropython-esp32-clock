import network, utime  # pylint: disable=import-error


def wifi_up(ssid, password):
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(ssid, password)
    tmo = 50
    while not sta_if.isconnected():
        utime.sleep_ms(100)
        tmo -= 1
        if tmo == 0:
            break


def telnet_up(username=None, password=None):
    return network.telnet.start(user=username or "m", password=password or "m")


def ftp_up(username=None, password=None):
    return network.ftp.start(user=username or "m", password=password or "m")


def mdns_up(unit_name, unit_description, bc_telnet=False, bc_ftp=False):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        raise Exception("Network not availabel")
    else:
        try:
            mdns = network.mDNS()
            mdns.start(unit_name, unit_description)

            if bc_telnet:  # broadcast telnet
                _ = mdns.addService(
                    "_ftp",
                    "_tcp",
                    21,
                    "MicroPython",
                    {
                        "board": "ESP32",
                        "service": "mPy FTP File transfer",
                        "passive": "True",
                    },
                )
            if bc_ftp:
                _ = mdns.addService(
                    "_telnet",
                    "_tcp",
                    23,
                    "MicroPython",
                    {"board": "ESP32", "service": "mPy Telnet REPL"},
                )
            # _ = mdns.addService('_http', '_tcp', 80, "MicroPython", {"board": "ESP32", "service": "mPy Web server"})
            print("mDNS started")
        except:
            print("mDNS not started")
