# The purpose of this script is to determine the source points for the stitched image
import numpy as np
import cv2
import os
from glob import glob

# Define image files path
image_files = glob(os.getcwd()+"*/*/*.JPG")
images = []

# Loop through files, load images, and store in an array
print("Stiching images")
for image in image_files:
    img = cv2.imread(image)
    images.append(img)

imageStitcher = cv2.Stitcher_create()

error, stitched_img = imageStitcher.stitch(images)

# Callback function for mouse events
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Display the coordinates on the console
        print(f'Coordinates: ({x}, {y})')

        # Draw a circle at the clicked point
        cv2.circle(stitched_img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow('Image', stitched_img)

        # Append the clicked point to the list of points
        points.append((x, y))

# Create a window and set the callback function
cv2.imshow('Image', stitched_img)
cv2.setMouseCallback('Image', click_event)

# List to store the points
points = []

# Wait for the user to click four points
while len(points) < 4:
    cv2.waitKey(1)

# Convert the list of points to NumPy array
points = np.array(points, dtype=np.float32)

# Close the image window
cv2.destroyAllWindows()

# Print the selected points
print('Selected Points:', points)