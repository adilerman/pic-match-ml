# import required libraries
import numpy as np
import cv2
from matplotlib import pyplot as plt

# read two input images
# Calculate the midpoint of the image
image_path = '/old/data/v5_crop/cropped_originals/border_removed_02011v.jpg.png'
original_image = cv2.imread(image_path)

height, width, _ = original_image.shape

midpoint = width // 2

# Split the image into two halves
left_image = cv2.cvtColor(original_image[:, :midpoint, :], cv2.COLOR_BGR2GRAY)
right_image = cv2.cvtColor(original_image[:, midpoint:, :], cv2.COLOR_BGR2GRAY)


# Create a StereoSGBM object (Semi-Global Block Matching)
stereo = cv2.StereoSGBM_create(numDisparities=16, blockSize=5)

# Compute the disparity map
disparity_map = stereo.compute(left_image, right_image)

# Normalize the disparity map for better visualization
disparity_map = cv2.normalize(disparity_map, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)

# Display the images and the depth map
cv2.imshow('Left Image', left_image)
cv2.imshow('Right Image', right_image)
cv2.imshow('Disparity Map', disparity_map)
cv2.waitKey(0)
cv2.destroyAllWindows()