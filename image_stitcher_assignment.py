import numpy as np
import cv2
import os
from glob import glob

# Define image files path
image_files = glob(os.getcwd()+"*/*/*.JPG")
images = []

# Loop through files, load images, and store in an array
print("Beginning image stitching.")
for image in image_files:
    img = cv2.imread(image)
    images.append(img)
    
imageStitcher = cv2.Stitcher_create()

error, stitched_img = imageStitcher.stitch(images)

# if there's no error, continue processing stitched image
if not error:    
    print("Stitching complete. Starting transformation.")
    # These are the coordinates of the four corners
    # of the stitched image, using a mouse click-event
    src_points = np.float32([[3340, 54], [12116, 50], [15629, 6042], [97, 6313]])
    
    # Flatten the image
    width, height = 6000, 6000  # Chosen through trial and error
    
    # Destination points to flatten the image
    dst_points = np.array([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]], dtype=np.float32)

    # Apply transformation to stitched image
    M = cv2.getPerspectiveTransform(src_points, dst_points)
    transformed_img = cv2.warpPerspective(stitched_img, M, (width, height)) 

    print("Transformation complete. Starting crop.")

    # Begin image crop
    # Convert transformed image to grayscale
    gray = cv2.cvtColor(transformed_img, cv2.COLOR_BGR2GRAY)

    # Finding the bounding box to crop
    contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Crop the image using the bounding box
    cropped_image = transformed_img[y:y + h, x:x + w]

    print("Completed crop. Saving image.")

    # Result
    cv2.imwrite('result.jpg', cropped_image)

    print("Image saved.")

else:
    print("Images could not be stitched!")
    print("Likely not enough keypoints being detected!")