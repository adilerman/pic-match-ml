import os
import cv2
from my_image import MyImage

import glob

files = glob.glob(f"/Users/adilerman/PycharmProjects/pic-match-ml/data/old_scraped/original/*.jpg")
for file in files:
    file_name = os.path.basename(file)
    img = MyImage(file)
    cv2.imwrite(f'/Users/adilerman/PycharmProjects/pic-match-ml/data/old_scraped/grey/{file_name}', img.img_grey)
