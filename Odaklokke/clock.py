"All time and date related functionality"

import machine, utime, network  # pylint: disable=import-error

from config import TIMEZONE, NTP_SERVER

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

ADVICE = [
    (0.0, 6.4, b"Sovetid :D"),
    (6.5, 7.9, b"Tid for \xe5 st\xe5 opp"),
    (8.0, 13.9, b"G\xe5 til skolen"),
    (14.0, 15.9, b"Leksetid"),
    (16.0, 18.9, b"Middag! Nam, nam!"),
    (19.0, 19.9, b"Gj\xf8r klar til kvelden"),
    (20.0, 24.0, b"Sovetid :D"),
]


def ntp_sync() -> bool:
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        raise Exception("Network not availabel")
    rtc = machine.RTC()
    rtc.ntp_sync(server=NTP_SERVER, tz=TIMEZONE, update_period=60 * 60 * 24)
    return rtc.synced()


def round_to_nearest(n: int, m: int) -> int:
    "Round `n` to nearest multiple of `m`"
    r = n % m
    return n + m - r if r + r >= m else n - r


def now_human_repr() -> tuple:
    # Return the current time as tuple: (2020, 5, 3, 14, 34, 45, 1, 124)
    stamp = utime.localtime()
    timestamp = (stamp[3], stamp[4], stamp[5])
    nearest_five = round_to_nearest(timestamp[1], 5)
    current_hour = timestamp[0] % 12
    return (
        timestamp,
        MNEMONICS[nearest_five]
        + HOURS[current_hour if nearest_five < 20 else current_hour + 1],
    )


def get_advice() -> bytes:
    "Look at the hour and give advice "
    stamp = utime.localtime()
    _hr = stamp[3] + float(stamp[4] / 60.0)
    for (hr_start, hr_end, advice) in ADVICE:
        if hr_start < _hr < hr_end:
            return advice
