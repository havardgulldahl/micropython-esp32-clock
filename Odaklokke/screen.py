import display  # pylint: disable=import-error

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
        tft.line(i, 240, i, 240 - RAINBOW_HEIGHT, color)

    tft.set_fg(0x000000)
    tft.font("ubuntu28.fon")  # ubuntu regular, with norwegian characters
    return tft


def write_line(tft, text: bytes, lineno: int) -> None:
    "Write text to given line"
    x = tft.CENTER
    _fontHeight = tft.fontSize()[1]
    y = _fontHeight * lineno + RAINBOW_HEIGHT
    # first, blank out line (colors are inverted)
    tft.rect(0, y, 300, _fontHeight, tft.BLACK, tft.BLACK)
    # now, write text (colors are inverted)
    tft.text(x, y, text, tft.WHITE)
