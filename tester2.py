import cv2

import image_comparer
from my_image import MyImage

img = MyImage('/Users/adilerman/PycharmProjects/pic-match-ml/data/v5_crop/cropped_originals/border_removed_02035v.jpg.png')
height, width = img.img_grey.shape
if width % 2 != 0:
    width = width - 1
    img.img_grey = img.img_grey[:, :-1]
image_comparer = image_comparer.ImageComparer()
left_half = img.img_grey[:, :width // 2]
right_half = img.img_grey[:, width // 2:]
cv2.imwrite('left_half.jpg', left_half)
cv2.imshow("left_half", left_half)
cv2.waitKey()
cv2.imwrite('right_half.jpg', right_half)
cv2.imshow("right_half", right_half)
cv2.waitKey()
x = 5
is_matching = image_comparer.compare_images(MyImage('left_half.jpg'), MyImage('right_half.jpg'), print_matches=True)
# matches[os.path.basename(img1.path)][os.path.basename(img2_path)] = is_matching
