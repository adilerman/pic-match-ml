import glob
import os

import cv2


def get_image_class(retry=5):
    if retry <= 0:
        raise "wrong class entered"
    img_class = input("Please enter class name, a : image does not contain the object  b : image contains the object ")
    if img_class not in ('a', 'b'):
        print("Wrong class entered please enter a or b")
        get_image_class(retry=retry - 1)
    return img_class


class Labeler:
    def __init__(self, input_path, output_path):
        self.input_path = input_path
        self.output_path = output_path
        self.image_files = glob.glob(f'{input_path}*.jpg')

    def label_image(self, image_path):
        img = cv2.imread(image_path)
        x, y, w, h = cv2.selectROI("Select ROI", img, fromCenter=False, showCrosshair=True)
        cv2.destroyAllWindows()
        x2, y2 = x + w, y + h

        img_class = get_image_class()
        print(f'the class is {img_class} and the bounding box is ({x},{y}), ({x2},{y2})')
        image_file_name = os.path.basename(image_path)
        cv2.imwrite(f"{self.output_path}class_{img_class}_{image_file_name}", img)
        bb_file_name = os.path.splitext(f'class_{img_class}_{image_file_name}')[0] + '.bb'
        f = open(f'{self.output_path}{bb_file_name}', 'w')
        f.write(f"{x}_{y}_{x2}_{y2}")
        f.close()


if __name__ == "__main__":
    input_path = "/Users/adilerman/PycharmProjects/pic-match-ml/data/v6_roi/classifier/"
    output_path = "/Users/adilerman/PycharmProjects/pic-match-ml/data/v6_roi/labeled/"
    labeler = Labeler(input_path, output_path)
    for file in labeler.image_files:
        labeler.label_image(file)
