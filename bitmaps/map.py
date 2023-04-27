from PIL import Image
import math

ip_addresses = []
statuses = []

# Read the contents of the file
with open('icmp_responses.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        # Split the line into IP address and status
        ip, status = line.strip().split(',')
        ip_addresses.append(ip)
        statuses.append(int(status))

# Determine the size of the image
num_pixels = len(ip_addresses)
image_width = math.ceil(num_pixels ** 0.5)  # Adjusted width calculation

# Create a new blank image
image = Image.new('L', (image_width, image_width))

# Set the pixels based on the statuses
pixels = []
for status in statuses:
    if status == 0:
        pixel_value = 0
    elif status == 1:
        pixel_value = 255
    else:
        pixel_value = (255,0,0)
    
    pixels.append(pixel_value)

# Assign the pixel values to the image
image.putdata(pixels)

# Display the image
image.show()
