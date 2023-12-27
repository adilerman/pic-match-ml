import os
import cv2

import glob

output_path = '/old/data/v4/to_sift_512_real'
input_path = '/old/data/v4/to_sift_original_size'
size = (512, 512)
files = glob.glob(f"{input_path}/*.jpg")
for file in files:
    file_name = os.path.basename(file)
    print(file_name)
    if not os.path.isfile(f'output_path/{file_name}'):
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        if size:
            img = cv2.resize(img, size)
        cv2.imwrite(f'{output_path}/{file_name}', img)
