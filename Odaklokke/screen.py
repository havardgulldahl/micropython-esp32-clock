import display  # pylint: disable=import-error

_lasttext = None

RAINBOW_HEIGHT = 13  # in pixels


def setup():
    tft = display.TFT()
    tft.init(
        tft.ST7789,
        bgr=False,
        rot=tft.LANDSCAPE,
        miso=17,
        backl_pin=4,
        backl_on=1,
        mosi=19,
        clk=18,
        cs=5,
        dc=16,
        splash=False,
    )

    tft.setwin(20, 52, 320, 240)
    for i in range(0, 301):
        color = 0xFFFFFF - tft.hsb2rgb(i / 301 * 360, 1, 1)
        tft.line(i, 0, i, RAINBOW_HEIGHT, color)

    tft.set_fg(0x000000)
    tft.font("ubuntu.fon")  # ubuntu regular 32pt, with norwegian characters
    return tft


def write_text(tft, text):
    global _lasttext
    if _lasttext is not None:
        _x, _y, _text = _lasttext
        tft.textClear(_x, _y, _text)
    x = 120 - int(tft.textWidth(text) / 2)
    y = 67 - int(tft.fontSize()[1] / 2)
    tft.text(
        x, y, text, 0xFFFFFF,
    )
    _lasttext = (x, y, text)


def write_line_one(tft, text: bytes) -> None:
    "Write text to top line"
    x = tft.CENTER
    y = (tft.fontSize()[1] * 0) + RAINBOW_HEIGHT
    tft.text(x, y, text, 0xFFFFFF)


def write_line_two(tft, text: bytes) -> None:
    "Write text to second line"
    x = tft.CENTER
    y = (tft.fontSize()[1] * 1) + RAINBOW_HEIGHT
    tft.text(x, y, text, 0xFFFFFF)


def write_line_three(tft, text: bytes) -> None:
    "Write text to third line"
    x = tft.CENTER
    y = (tft.fontSize()[1] * 2) + RAINBOW_HEIGHT
    tft.text(x, y, text, 0xFFFFFF)


def write_line_four(tft, text: bytes) -> None:
    "Write text to bottom line"
    x = tft.CENTER
    y = (tft.fontSize()[1] * 3) + RAINBOW_HEIGHT
    tft.text(x, y, text, 0xFFFFFF)
