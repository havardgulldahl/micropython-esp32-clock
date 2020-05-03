"All time and date related functionality"

import machine, utime, network  # pylint: disable=import-error

from config import TIME_UTC_DIFF

HOURS = [
    b"midnatt",
    b"ett",
    b"to",
    b"tre",
    b"fire",
    b"fem",
    b"seks",
    b"sju",
    b"\xe5tte",
    b"ni",
    b"ti",
    b"elleve",
    b"tolv",
]

# b'\xf8\xD8\xe6\xC6\xe5\xc5' = "øØæÆåÅ"
MNEMONICS = {
    0: b"",
    5: b"fem over ",
    10: b"ti over ",
    15: b"kvart over ",
    20: b"ti p\xe5 halv ",
    25: b"fem p\xe5 halv ",
    30: b"halv ",
    35: b"fem over halv ",
    40: b"ti over halv ",
    45: b"kvart p\xe5 ",
    50: b"ti p\xe5 ",
    55: b"fem p\xe5 ",
    60: b"",
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
        MNEMONICS[nearest_five]
        + HOURS[current_hour if nearest_five < 20 else current_hour + 1],
    )
