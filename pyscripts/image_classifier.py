import glob

from common.utils import read_points_from_file, is_point_inside_box
from pyscripts import image_comparer
from pyscripts.my_image import MyImage


class ImageClassifier:
    def __init__(self, labeled_images_path):
        self.labeled_images_path = labeled_images_path + '/' if labeled_images_path[-1] != '/' else ''
        self.image_comparer = image_comparer.ImageComparer()
        self.labeled_images = glob.glob(f'{self.labeled_images_path}*.j*')  # get all images
        self.test_a, self.test_b = [], []
        for image_path in self.labeled_images:
            if 'class_a' in image_path:
                self.test_a.append(self.get_test_data(image_path))
            elif 'class_b' in image_path:
                self.test_b.append(self.get_test_data(image_path))

    def classify(self, test_image_path):
        test_image_obj = MyImage(test_image_path)
        a_scores, b_scores = self.collect_matching_points(test_image_obj)
        print(f'a_scores, b_scores {len(a_scores)} {len(b_scores)}')
        return self.find_class(a_scores, b_scores)

    @staticmethod
    def get_test_data(image_path):
        test_img_obj = MyImage(image_path)
        bounding_box_path = image_path.split('.')[-2] + '.bb'
        x1, y1, x2, y2 = read_points_from_file(bounding_box_path)
        relevant_keypoints = [point for point in test_img_obj.keypoints if is_point_inside_box(x1, y1, x2, y2, point.pt[0], point.pt[1])]
        # draw_points(test_img_obj.img, [point.pt for point in relevant_keypoints])
        test_data = {'image_path': image_path,
                     'image_obj': test_img_obj,
                     'bounding_box': [x1, y1, x2, y2],
                     'relevant_keypoints': relevant_keypoints}
        return test_data

    def collect_matching_points(self, test_image_obj):
        a_scores, b_scores = [], []
        for test_image_data in self.test_a:
            comparing_image_obj = MyImage(path=test_image_data['image_path'])
            a_scores.extend(self.score_match(test_image_obj, comparing_image_obj, test_image_data['relevant_keypoints']))
        for test_image_data in self.test_b:
            comparing_image_obj = MyImage(path=test_image_data['image_path'])
            b_scores.extend(self.score_match(test_image_obj, comparing_image_obj, test_image_data['relevant_keypoints']))
        return a_scores, b_scores

    def score_match(self, test_image_obj, comparing_image_obj, relevant_test_keypoints):
        matching_pints = []
        good_matches = self.image_comparer.find_best_matching_keypoints(test_image_obj.descriptors, comparing_image_obj.descriptors)
        fundamental_matrix, mask = self.image_comparer.create_fundamental_matrix(good_matches, test_image_obj.keypoints, comparing_image_obj.keypoints)
        if mask is None:
            print("No matching points.")
            return []
        inlier_matches = [match for mask_value, match in zip(mask.flatten().tolist(), good_matches) if mask_value == 1]
        for inlier_match in inlier_matches:
            point = comparing_image_obj.keypoints[inlier_match.trainIdx].pt
            if point in [relevant_test_keypoint.pt for relevant_test_keypoint in relevant_test_keypoints]:
                matching_pints.append(test_image_obj.keypoints[inlier_match.queryIdx].pt)
        return matching_pints

    @staticmethod
    def find_class(a_scores, b_scores):
        return 'a' if len(a_scores) > len(b_scores) else 'b'


if __name__ == "__main__":
    labeled_images_path = "/Users/adilerman/PycharmProjects/pic-match-ml/data/v6_roi/test1/labeled_data/"
    test_image_path = '/Users/adilerman/PycharmProjects/pic-match-ml/data/v6_roi/test1/labeled_data/test_b.jpeg'
    image_classifier = ImageClassifier(labeled_images_path)
    print(f"The image if of class {image_classifier.classify(test_image_path)}")
