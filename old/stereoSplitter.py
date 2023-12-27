import glob

import cv2
import numpy as np

import my_image
from image_comparer import ImageComparer


class StereoSplitter:
    def __init__(self, img: my_image.MyImage, output_save_path: str = None):
        self.output_save_path = output_save_path
        self.img = img
        self.sift = cv2.SIFT_create()

    def is_stereo_image(self, print_matches):
        ic = ImageComparer()
        matches, mask = ic.find_second_best_matches(self.img, self.img)
        ic.print_matching_points(self.img.img, self.img.img, print_matches=print_matches, mask=mask, good_matches=matches,
                                 keypoints1=self.img.keypoints, keypoints2=self.img.keypoints)
        if mask is None:
            return []
        return [match for idx, match in enumerate(matches) if mask.flatten().tolist()[idx]]


stereo_image_path = '/old/data/v5_crop/cropped_originals/border_removed_03406v.jpg.png'
non_stereo_image_path = '/old/data/v5_crop/cropped_originals/border_removed_00056v.jpg.png'
for image_path in glob.glob('/old/data/v5_crop/cropped_originals/*'):
    my_image_obj = my_image.MyImage(image_path, params=None)
    stereo_spliter = StereoSplitter(my_image_obj)
    image_inner_matches = stereo_spliter.is_stereo_image(print_matches=False)
    if len(image_inner_matches) > 20:
        height, width = my_image_obj.img_grey.shape
        if width % 2 != 0:
            width = width - 1
            my_image_obj.img_grey = my_image_obj.img_grey[:, :-1]
            # Split the image into left and right halves
        left_half = my_image_obj.img_grey[:, :width // 2]
        right_half = my_image_obj.img_grey[:, width // 2:]

        # Calculate the absolute pixel-wise difference between the left and right halves
        diff = cv2.absdiff(left_half, right_half)

        # Calculate the average difference
        avg_difference = np.mean(diff)
        print(f"num matches : {len(image_inner_matches)}, avg diff:{avg_difference} path: {image_path}")
        if avg_difference < 50:
            cv2.imshow('matching??', cv2.imread(image_path))
            cv2.waitKey(0)
            cv2.destroyAllWindows()
x = 5
