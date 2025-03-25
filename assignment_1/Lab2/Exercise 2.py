import board
import time
import analogio
import terminalio
from adafruit_display_text import label

light = analogio.AnalogIn(board.D0)

display = board.DISPLAY
font = terminalio.FONT
text_area = label.Label(font, scale=3)
text_area.x = 32
text_area.y = 120

display.root_group = text_area

while True:
    voltage = light.value * 3.3 / 65535
    text_area.text = str(voltage) + ' V'
    time.sleep(0.1)
