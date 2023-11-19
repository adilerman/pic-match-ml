import glob

import cv2
import numpy as np

import image_comparer
from my_image import MyImage


def draw_heatmap(image, points):
    # Define the number of rows and columns for the grid
    num_rows, num_cols = 10, 10  # 1000 squares in a 10x10 grid
    # Calculate the width and height of each square
    square_width = image.shape[1] // num_cols + 1
    square_height = image.shape[0] // num_rows + 1
    heatmap = np.zeros((num_rows, num_cols), dtype=np.uint8)
    # Iterate through the list of points and increment the corresponding region in the heatmap
    for point in points:
        x, y = map(int, point)  # Convert floating-point coordinates to integers
        if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
            heatmap[x // square_width, y // square_height] += 1
    heatmap = heatmap * 255.0 / heatmap.max()
    # heatmap = heatmap.astype(int)
    # Create a red color image
    red_color = np.zeros_like(image)
    red_color[:, :, 2] = 255  # Set the red channel to 255 (full red)
    heatmap_on_image = image.copy()
    for y in range(image.shape[0]):
        for x in range(image.shape[1]):
            heatmap_on_image[y, x] = (0, 0, heatmap[x // square_width, y // square_height])
    # Create the overlay by combining the image and the red color based on the heatmap
    overlay = cv2.addWeighted(image, 0.3, heatmap_on_image, 0.7, 6.6)
    # Display the resulting image with the heatmap overlay
    cv2.imshow('Heatmap Overlay', overlay)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def draw_points(image, points):
    # Define the color and size of the points
    point_color = (0, 0, 255)  # Red color in BGR format (OpenCV uses BGR)
    point_size = 1  # Size of the point
    # Iterate through the list of points and draw each point on the image
    for point in points:
        x, y = map(int, point)  # Convert floating-point coordinates to integers
        cv2.circle(image, (x, y), point_size, point_color, -1)  # Draw a filled circle
    # Display the image with the drawn points
    cv2.imshow('Image with Points', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


class RoiSift:
    def __init__(self, input_image: str, comparing_images: list = None):
        self.input_img = input_image
        self.input_img_obj = MyImage(self.input_img)
        self.comparing_images = comparing_images
        self.image_comparer = image_comparer.ImageComparer()

    def collect_matching_points(self):
        matching_pints = []
        for comparing_image in self.comparing_images:
            comparing_image_obj = MyImage(path=comparing_image)
            good_matches = self.image_comparer.find_best_matching_keypoints(self.input_img_obj.descriptors, comparing_image_obj.descriptors)
            fundamental_matrix, mask = self.image_comparer.create_fundamental_matrix(good_matches, self.input_img_obj.keypoints, comparing_image_obj.keypoints)
            if mask is None:
                # print("The images represent different objects.")
                return False
            inlier_matches = [match for mask_value, match in zip(mask.flatten().tolist(), good_matches) if mask_value == 1]
            for inlier_match in inlier_matches:
                matching_pints.append(self.input_img_obj.keypoints[inlier_match.queryIdx].pt)
        # draw_points(image=self.input_img_obj.img, points=matching_pints)
        return matching_pints
        # draw_heatmap(image=self.input_img_obj.img, points=matching_pints)


input_image = '/Users/adilerman/PycharmProjects/pic-match-ml/data/v6_roi/cropped/border_removed_a_8_input.jpg'
comparing_images = [img for img in glob.glob('/Users/adilerman/PycharmProjects/pic-match-ml/data/v6_roi/cropped/*') if 'input' not in img]
roi_sift = RoiSift(input_image=input_image, comparing_images=comparing_images)
matching_pints = roi_sift.collect_matching_points()

cnt = 0
matched_keypoints = set()
for keypoint in roi_sift.input_img_obj.keypoints:
    if keypoint.pt in matching_pints:
        cnt += 1
        matched_keypoints.add(keypoint.pt)
unmatched_keypoints = [point.pt for point in roi_sift.input_img_obj.keypoints if point.pt not in matched_keypoints]
draw_heatmap(image=roi_sift.input_img_obj.img, points=unmatched_keypoints)
x = 4
