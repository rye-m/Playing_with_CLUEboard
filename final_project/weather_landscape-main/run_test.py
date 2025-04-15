import os
import sys


from weather_landscape import WeatherLandscape

# Check if there are any arguments
if len(sys.argv) < 1:
    print("Usage: python script.py <argument1> ")
    sys.exit(1)

bmp_index = sys.argv[1]





w = WeatherLandscape()

fn = w.SaveImage(bmp_index)

print("Saved",fn)

    
