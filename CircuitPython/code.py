import time
import board
import displayio
import terminalio
from adafruit_display_text import label
from adafruit_lsm6ds.lsm6ds33 import LSM6DS33
from adafruit_clue import clue

import busio
import adafruit_vcnl4040

import adafruit_apds9960.apds9960

# i2c = busio.I2C(board.SCL, board.SDA)
# i2c = board.I2C()  # uses board.SCL and board.SDA
i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
sensor_d = adafruit_vcnl4040.VCNL4040(i2c)


# Constants
GRAVITY = 9.81  # m/s²
UPDATE_INTERVAL = 0.1  # seconds
CALIBRATION_SAMPLES = 100
LOW_PASS_ALPHA = 0.1  # Filter coefficient (0-1)
# i2c = board.I2C()
sensor = LSM6DS33(i2c)

while True:
    print("Proximity:", sensor_d.proximity)
    # print("Light: %d lux" % sensor_d.lux)
    time.sleep(0.01)


# Setup display
display = board.DISPLAY
font = terminalio.FONT
splash = displayio.Group()
display.root_group = splash

title_text = label.Label(font, text="Speedometer", x=10, y=32, scale=3)
speed_text = label.Label(font, text="  0.0 m/s", x=10, y=120, scale=3)
splash.append(title_text)
splash.append(speed_text)

# text_area.x = 32
# text_area.y = 120
# text_area.text = str(voltage) + ' V'


# Initialize variables
last_time = time.monotonic()
speed = 0.0
filtered_x, filtered_y, filtered_z = 0, 0, 0

# Main loop
while True:
    current_time = time.monotonic()
    dt = current_time - last_time

    if dt >= UPDATE_INTERVAL:
        # Read accelerometer
        x, y, z = clue.gyro

        # Apply low-pass filter
        filtered_x = LOW_PASS_ALPHA * x + (1 - LOW_PASS_ALPHA) * filtered_x
        filtered_y = LOW_PASS_ALPHA * y  + (1 - LOW_PASS_ALPHA) * filtered_y
        filtered_z = LOW_PASS_ALPHA * z + (1 - LOW_PASS_ALPHA) * filtered_z

        # Calculate magnitude of acceleration (ignoring gravity)
        accel_magnitude = (filtered_x**2 + filtered_y**2)**0.5

        # Only integrate if acceleration is above a threshold to avoid drift
        if abs(accel_magnitude) > 0.2:
            # Integrate acceleration to get velocity
            if x * y >0:
                speed += accel_magnitude * dt
            else:
                speed -= accel_magnitude * dt


        # Apply friction/damping to gradually bring speed to zero
        #speed *= 0.95

        # Update display
        speed_text.text = f"  {speed:.2f} m/s"

        # Update NeoPixel color based on speed (optional)
        # Green at low speeds, transitions to yellow, then red at high speeds
        if speed < 2:
            r, g, b = int(speed * 100), 255, 0
        else:
            r, g, b = 255, max(0, int(255 - (speed - 2) * 50)), 0
        clue.pixel.fill((min(255, r), min(255, g), min(255, b)))

        last_time = current_time

    # Check for button press to reset
    if clue.button_a:
        speed = 0.0
        speed_text.text = f"  {speed:.2f} m/s"
        clue.pixel.fill((0, 255, 0))
        time.sleep(0.2)  # Debounce

    time.sleep(0.01)  # Small delay to avoid hogging the CPU
