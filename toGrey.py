import os
import cv2

import glob

files = glob.glob(f"/Users/shayarbiv/Downloads/old2new/testB/*.jpg")
for file in files:
    file_name = os.path.basename(file)
    print(file_name)
    if not os.path.isfile(f'/Users/shayarbiv/Downloads/old2new/testB_grey/{file_name}'):
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(f'/Users/shayarbiv/Downloads/old2new/testB_grey/{file_name}', img)
