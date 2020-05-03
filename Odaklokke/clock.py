"All time and date related functionality"

import machine, utime, network  # pylint: disable=import-error

from config import TIME_UTC_DIFF

HOURS = [
    "midnatt",
    "ett",
    "to",
    "tre",
    "fire",
    "fem",
    "seks",
    "sju",
    "åtte",
    "ni",
    "ti",
    "elleve",
    "tolv",
]

MNEMONICS = {
    5: "fem over",
    10: "ti over",
    15: "kvart over",
    20: "ti på halv",
    25: "fem på halv",
    30: "halv",
    35: "fem over halv",
    40: "ti over halv",
    45: "kvart på",
    50: "ti på",
    55: "fem på",
}


def ntp_sync():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        raise Exception("Network not availabel")
    rtc = machine.RTC()
    rtc.ntp_sync(server="no.pool.ntp.org", tz="CEST")
    return rtc.synced()


def round_to_nearest(n: int, m: int) -> int:
    "Round `n` to nearest multiple of `m`"
    r = n % m
    return n + m - r if r + r >= m else n - r


def now_human_repr() -> tuple:
    # Return the current time as tuple: (2020, 5, 3, 14, 34, 45, 1, 124)
    stamp = utime.localtime()
    timestamp = (stamp[3] + TIME_UTC_DIFF, stamp[4], stamp[5])
    nearest_five = round_to_nearest(timestamp[1], 5)
    current_hour = timestamp[0] % 12
    return (
        timestamp,
        "{} {}".format(
            MNEMONICS[nearest_five],
            HOURS[current_hour if nearest_five < 20 else current_hour + 1],
        ),
    )
