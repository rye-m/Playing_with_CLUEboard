# rename this file to code.py to make it run on your Clue

import time
import analogio
import board

light = analogio.AnalogIn(board.D0)

while True:
    print((light.value,))
    time.sleep(0.1)
