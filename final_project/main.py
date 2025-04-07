from PIL import Image, ImageDraw
import csv

def create_xy_plot(csv_filename, output_filename="xy_plot.png", image_size=(800, 600), margin=150):
    # Read x,y coordinates from CSV file
    x_coords = []
    y_coords = []
    
    with open(csv_filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        # Skip header row if exists (assuming first row has headers)
        header = next(csv_reader, None)
        
        for row in csv_reader:
            if len(row) >= 2:  # Ensure row has at least 2 values
                try:
                    x = float(row[0])
                    y = float(row[1])
                    x_coords.append(x)
                    y_coords.append(y)
                except ValueError:
                    print(f"Skipping invalid data: {row}")
    
    if not x_coords or not y_coords:
        print("No valid data points found in CSV.")
        return
    
    # Find min and max values to scale the plot
    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)
    
    # Calculate scaling factors to fit within the image (with margins)
    width, height = image_size
    usable_width = width - 2 * margin
    usable_height = height - 2 * margin
    
    # Handle case where all x or y values are the same
    x_range = max_x - min_x
    if x_range == 0:
        x_range = 1  # Avoid division by zero
    
    y_range = max_y - min_y
    if y_range == 0:
        y_range = 1  # Avoid division by zero
    
    x_scale = usable_width / x_range
    y_scale = usable_height / y_range
    
    # Create a new image (white background)
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)
    
    # Draw axes
    draw.line([(margin, height - margin), (width - margin, height - margin)], fill="black", width=1)  # X-axis
    draw.line([(margin, margin), (margin, height - margin)], fill="black", width=1)  # Y-axis
    
    # Scale coordinates to fit within the plot area
    # Note: we invert y-coordinates because image coordinates have origin at top left
    scaled_coords = []
    for x, y in zip(x_coords, y_coords):
        scaled_x = margin + (x - min_x) * x_scale
        # Invert y-axis (subtract from height) to make higher values appear higher in the plot
        scaled_y = height - margin - (y - min_y) * y_scale
        scaled_coords.append((scaled_x, scaled_y))
    
    # Draw lines connecting the points
    if len(scaled_coords) > 1:
        draw.line(scaled_coords, fill="blue", width=2)
    
    # Draw points
    for x, y in scaled_coords:
        # Draw a small circle for each point
        radius = 4
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill="red")
    
    # Draw tick marks and labels (simplified)
    font_size = 10
    # X-axis ticks and labels (simplified)
    for i in range(5):
        x_val = min_x + (i * x_range / 4)
        x_pos = margin + (i * usable_width / 4)
        y_pos = height - margin + 10
        draw.line([(x_pos, height - margin - 3), (x_pos, height - margin + 3)], fill="black", width=1)
        draw.text((x_pos - 10, y_pos), f"{x_val:.1f}", fill="black")
    
    # Y-axis ticks and labels (simplified)
    for i in range(5):
        y_val = min_y + (i * y_range / 4)
        y_pos = height - margin - (i * usable_height / 4)
        draw.line([(margin - 3, y_pos), (margin + 3, y_pos)], fill="black", width=1)
        draw.text((margin - 25, y_pos - 5), f"{y_val:.1f}", fill="black")
    
    # Save image
    image.save(output_filename)
    print(f"Plot saved as {output_filename}")
    
    # Display image
    image.show()


# Usage
if __name__ == "__main__":
    # Replace 'data.csv' with your actual CSV filename
    create_xy_plot('/Users/ryem/Desktop/Cornell_Tech/fun/Playing_with_CLUEboard/final_project/data/sample_altitude.csv')