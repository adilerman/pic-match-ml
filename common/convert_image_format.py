import os
import cv2


class ImageConverter:
    def __init__(self, input_dir, output_dir, input_format, output_format):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.input_format = input_format
        self.output_format = output_format

    def create_output_dir(self):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)

    def convert_images(self):
        self.create_output_dir()
        image_files = [f for f in os.listdir(self.input_dir) if f.endswith(self.input_format)]
        for image_file in image_files:
            input_path = os.path.join(self.input_dir, image_file)
            output_path = os.path.join(self.output_dir, os.path.splitext(image_file)[0] + '.' + self.output_format)
            # Read and convert the image using OpenCV
            image = cv2.imread(input_path)
            cv2.imwrite(output_path, image)
            print(f"Converted: {input_path} -> {output_path}")
