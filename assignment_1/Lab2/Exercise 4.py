import board
import displayio
from adafruit_clue import clue

display = board.DISPLAY

clean = displayio.OnDiskBitmap('/clean.bmp')
dirty = displayio.OnDiskBitmap('/dirty.bmp')

image_view = displayio.TileGrid(clean, pixel_shader=clean.pixel_shader)

window = displayio.Group()
window.append(image_view)

display.root_group = window

while True:
    if clue.button_b:
        image_view.bitmap = dirty
    if clue.button_a:
        image_view.bitmap = clean
