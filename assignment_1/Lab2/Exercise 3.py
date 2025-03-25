import board
import displayio
import terminalio
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33
from adafruit_display_text import label

i2c = board.I2C()
sensor = LSM6DS33(i2c)

display = board.DISPLAY
font = terminalio.FONT
x_label = label.Label(font, scale=3)
x_label.y = 92
y_label = label.Label(font, scale=3)
y_label.y = 120
z_label = label.Label(font, scale=3)
z_label.y = 148

window = displayio.Group()
window.append(x_label)
window.append(y_label)
window.append(z_label)
display.root_group = window

while True:
    x, y, z = sensor.acceleration
    x_label.text = 'X: ' + str(x)
    y_label.text = 'Y: ' + str(y)
    z_label.text = 'Z: ' + str(z)
