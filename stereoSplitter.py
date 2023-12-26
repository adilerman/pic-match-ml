import glob
import os
import cv2
from tqdm import tqdm


class Image:
    def __init__(self, path, params=None):
        self.path = path
        self.img = self.read_img_gray()
        self.keypoints, self.descriptors = self.get_keypoints_and_descriptors(params)
        self.matches = []

    def read_img(self):
        return cv2.imread(self.path)

    def read_img_gray(self):
        img = self.read_img()
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def create_sift(params):
        if params:
            return cv2.SIFT_create(**params)
        return cv2.SIFT_create()

    def split_image_to_two(self):
        height, width = self.img.shape
        if width % 2 != 0:
            width = width - 1
            self.img = self.img[:, :-1]
            # Split the image into left and right halves
        left_half = self.img[:, :width // 2]
        right_half = self.img[:, width // 2:]
        return left_half, right_half

    def get_keypoints_and_descriptors(self, params=None):
        sift = self.create_sift(params)
        return sift.detectAndCompute(self.img, None)

    def show_img(self):
        cv2.imshow('image', self.img)
        cv2.waitKey(0)

    def add_match(self, img):
        self.matches.append(img)


class StereoSplitter:
    def __init__(self, img: Image):
        self.matcher = cv2.BFMatcher_create()
        # self.matcher = cv2.FlannBasedMatcher_create()
        self.img = img

    def is_stereo_image(self, print_matches):
        # ic = ImageComparer()
        # matches = ic.find_matches_for_stereo(self.img, self.img)
        matches = self.find_matches(self.img, self.img)
        # matches, mask = ic.find_second_best_matches(self.img, self.img)
        # ic.print_matching_points(self.img.img, self.img.img, print_matches=print_matches, mask=mask, good_matches=matches,
        #                          keypoints1=self.img.keypoints, keypoints2=self.img.keypoints)
        return matches
        # if mask is None:
        #     return []
        # return [match for idx, match in enumerate(matches) if mask.flatten().tolist()[idx]]

    def find_matches(self, img1, img2):
        matches = self.matcher.knnMatch(img1.descriptors, img2.descriptors, k=3)
        good_matches = []
        for n_1, n_2, n_3 in matches:
            if (img2.keypoints[n_1.trainIdx] == img1.keypoints[n_1.queryIdx]) and \
                    ((1.1 * img2.keypoints[n_2.trainIdx].pt[1] > img1.keypoints[n_2.queryIdx].pt[1]) and
                     (img1.keypoints[n_2.queryIdx].pt[1] > 0.9 * img2.keypoints[n_2.trainIdx].pt[1])) and \
                    n_3.distance > 1.28 * n_2.distance:
                good_matches.append(n_2)
        return good_matches


def run_image(image_path):
    image_obj = Image(image_path, params=None)
    stereo_splitter = StereoSplitter(image_obj)
    image_inner_matches = stereo_splitter.is_stereo_image(print_matches=False)
    if len(image_inner_matches) > 410:
        return True
        # print(f"Found stereo image: {os.path.basename(image_path)}, number of matches : {len(image_inner_matches)}")
        #         if len(image_inner_matches) > 410:
        #             cv2.imshow('matching??', cv2.imread(image_path))
        #             cv2.waitKey(0)
        #             cv2.destroyAllWindows()
    return False


def main():
    path = input('Enter file or folder path\n')
    counter = 0
    counter_st = 0
    if os.path.isdir(path):
        image_list = glob.glob(os.path.join(path, '*'))
        for image_path in tqdm(image_list):
            stereo = run_image(image_path)
            counter += 1 if stereo else 0
            counter_st += 1 if (stereo and image_path.endswith('_st.jpg')) else 0
    else:
        run_image(path)
    print(f'Count of images that are suspected sterep: {counter}')
    print(f'Count of actual stereo images out of them: {counter_st}')
    return


if __name__ == '__main__':
    main()
