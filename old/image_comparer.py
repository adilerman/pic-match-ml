import cv2
import numpy as np
from my_image import MyImage


class ImageComparer:
    def __init__(self, params=None):
        self.matcher = params['matcher']() if params else cv2.FlannBasedMatcher_create()
        self.threshold = params['threshold'] if params else 22

    @staticmethod
    def to_greyscale(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray

    def find_second_best_matches(self, img1, img2):
        matches = self.matcher.knnMatch(img1.descriptors, img2.descriptors, k=3)
        # Apply ratio test to filter good matches
        good_matches = []
        for n_1, n_2, n_3 in matches:
            if n_1.distance > 0.75 * n_2.distance and n_2.distance < 0.75 * n_3.distance:
                good_matches.append(n_1)
                good_matches.append(n_2)
        matches = good_matches
        fundamental_matrix, mask = self.create_fundamental_matrix(good_matches, img1.keypoints, img2.keypoints)
        return matches, mask

    def compare_images(self, img1, img2, print_matches=False):
        # Perform feature matching
        good_matches = self.find_best_matching_keypoints(img1.descriptors, img2.descriptors)
        fundamental_matrix, mask = self.create_fundamental_matrix(good_matches, img1.keypoints, img2.keypoints)
        if mask is None:
            # print("The images represent different objects.")
            return False
        inliers = np.sum(mask)
        # Compare number of inliers with threshold
        if inliers >= self.threshold:
            self.print_matching_points(img1.img, img2.img, print_matches, mask, good_matches, img1.keypoints, img2.keypoints)
            # print("The images represent the same objects.")
            return True
        else:
            # print("The images represent different objects.")
            return False

    def find_best_matching_keypoints(self, descriptors1, descriptors2):
        matches = self.matcher.knnMatch(descriptors1, descriptors2, k=2)
        # Apply ratio test to filter good matches
        good_matches = []
        for n_1, n_2 in matches:
            if n_1.distance < 0.85 * n_2.distance:  # and n_2.distance < 200:
                good_matches.append(n_1)
        matches = good_matches
        return matches

    @staticmethod
    def create_fundamental_matrix(good_matches, keypoints1, keypoints2):
        # Extract keypoint coordinates for good matches
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        # Use RANSAC to estimate fundamental matrix
        fundamental_matrix, mask = cv2.findFundamentalMat(src_pts, dst_pts, cv2.RANSAC, 9.0)
        return fundamental_matrix, mask

    @staticmethod
    def print_matching_points(img1, img2, print_matches, mask, good_matches, keypoints1, keypoints2):
        if print_matches:
            draw_params = dict(matchColor=(0, 0, 255), singlePointColor=None, matchesMask=mask.flatten().tolist(), flags=2)
            match_img = cv2.drawMatches(img1, keypoints1, img2, keypoints2, good_matches, None, **draw_params)
            cv2.imshow("Good Matches", match_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    ic = ImageComparer()
    img1 = MyImage('data/images/original/test/3835-_flat.jpg')
    img2 = MyImage('data/images/original/test/3836-_flat.jpg')
    ic.compare_images(img1, img2, print_matches=False)
