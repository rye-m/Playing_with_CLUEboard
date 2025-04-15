#!/bin/bash

# clean up the tmp/output directory
rm -rf ~/Desktop/Cornell_Tech/fun/Playing_with_CLUEboard/final_project/weather_landscape-main/tmp/output/*.bmp


# run run_test.py for N times to generate N bmp images
for i in $(seq -f "%03g" 1 5); do
uv run run_test.py $i #> /dev/null 2>&1
done



# Convert all BMP files in the current directory to GIF format
cd ~/Desktop/Cornell_Tech/fun/Playing_with_CLUEboard/final_project/weather_landscape-main/tmp/output/

ffmpeg -framerate 3 -y -i  test_%03d.bmp test_output.gif > /dev/null 2>&1


# Check if the conversion was successful
if [ $? -eq 0 ]; then
echo "Converted successfully to test_output.gif"
else
echo "Failed to convert BMP files to GIF."
fi
