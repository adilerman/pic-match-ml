import cv2
import numpy as np

THRESHOLD = 22


def show_img(img):
    cv2.imshow('image', img)
    cv2.waitKey(0)


class ImageComparer:
    def __init__(self):
        self.sift = cv2.SIFT_create()
        self.matcher = cv2.FlannBasedMatcher_create()

    @staticmethod
    def to_greyscale(img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray

    def compare_images(self, img1, img2, print_matches=False):
        img1_grey = ic.to_greyscale(img1)
        img2_grey = ic.to_greyscale(img2)

        # Detect keypoints and compute descriptors
        keypoints1, descriptors1 = self.sift.detectAndCompute(img1_grey, None)
        keypoints2, descriptors2 = self.sift.detectAndCompute(img2_grey, None)
        # Perform feature matching
        good_matches = self.find_best_matching_keypoints(descriptors1, descriptors2)
        fundamental_matrix, mask = self.create_fundamental_matrix(good_matches, keypoints1, keypoints2)
        if mask is None:
            print("The images represent different objects.")
            return False
        inliers = np.sum(mask)
        self.print_matching_points(print_matches, mask, good_matches, keypoints1, keypoints2)
        # Compare number of inliers with threshold
        if inliers >= THRESHOLD:
            print("The images represent the same objects.")
        else:
            print("The images represent different objects.")

    def find_best_matching_keypoints(self, descriptors1, descriptors2):
        matches = self.matcher.knnMatch(descriptors1, descriptors2, k=2)
        # Apply ratio test to filter good matches
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
        return good_matches

    @staticmethod
    def create_fundamental_matrix(good_matches, keypoints1, keypoints2):
        # Extract keypoint coordinates for good matches
        src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        # Use RANSAC to estimate fundamental matrix
        fundamental_matrix, mask = cv2.findFundamentalMat(src_pts, dst_pts, cv2.RANSAC, 5.0)
        return fundamental_matrix, mask

    @staticmethod
    def print_matching_points(print_matches, mask, good_matches, keypoints1, keypoints2):
        if print_matches:
            draw_params = dict(matchColor=(0, 0, 255), singlePointColor=None, matchesMask=mask.flatten().tolist(), flags=2)
            match_img = cv2.drawMatches(img1, keypoints1, img2, keypoints2, good_matches, None, **draw_params)
            cv2.imshow("Good Matches", match_img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()


if __name__ == '__main__':
    ic = ImageComparer()
    img1 = cv2.imread('./data/images/3835-_flat.jpg')
    img2 = cv2.imread('./data/images/3836-_flat.jpg')
    ic.compare_images(img1, img2, True)

