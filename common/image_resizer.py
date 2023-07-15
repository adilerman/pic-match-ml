import cv2
import os


class ImageResizer:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def resize_images(self):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

        for image_file in os.listdir(self.input_dir):
            image = cv2.imread(os.path.join(self.input_dir, image_file))
            resized_image = cv2.resize(image, (640, 480))
            cv2.imwrite(os.path.join(self.output_dir, image_file), resized_image)
