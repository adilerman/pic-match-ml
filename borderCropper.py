import glob
import os

import cv2
import numpy as np
import my_image


class BorderCropper:
    def __init__(self, img: my_image.MyImage, output_save_path: str):
        self.output_save_path = output_save_path
        self.img = img

    def crop_border(self):
        try:
            # Apply Sobel operator to find edges
            sobel_x = cv2.Sobel(self.img.img_grey, cv2.CV_64F, 1, 0, ksize=3)
            sobel_y = cv2.Sobel(self.img.img_grey, cv2.CV_64F, 0, 1, ksize=3)
            # Calculate gradient magnitude
            gradient_magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
            # Threshold to find edges
            threshold = 100  # Adjust this value to suit your img
            border_edges = cv2.threshold(gradient_magnitude, threshold, 255, cv2.THRESH_BINARY)[1]
            # Find the coordinates of non-zero (edge) pixels
            non_zero_pixels = cv2.findNonZero(border_edges)
            # Get the bounding box around the edges
            x, y, w, h = cv2.boundingRect(non_zero_pixels)
            # Crop the original self.img to remove the border
            border_removed_img = self.img.img_grey[y:y + h, x:x + w]
            # Save the resulting self.img
            cv2.imwrite(f"{self.output_save_path}/border_removed_{os.path.basename(self.img.path)}", border_removed_img)
        except:
            print(os.path.basename(self.img.path))
            return os.path.basename(self.img.path)


files = glob.glob('/Users/adilerman/PycharmProjects/pic-match-ml/data/old_scraped/original/*')
failed = []
for file in files:
    my_image_obj = my_image.MyImage(file, params=None)
    bc = BorderCropper(img=my_image_obj, output_save_path='/Users/adilerman/PycharmProjects/pic-match-ml/data/v5_crop/cropped_originals')
    failed.append(bc.crop_border())
print(failed)
x=5