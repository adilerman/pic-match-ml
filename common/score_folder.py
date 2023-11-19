from collections import defaultdict

from common.utils import recursive_ls, get_all_pairs
from image_comparer import ImageComparer
from my_image import MyImage
import os


def score_sift(y_pred, y_test):
    false_positive = 0
    false_negative = 0
    true_positive = 0
    true_negative = 0
    for img1, matches in y_test.items():
        if 'DS_Store' in img1:
            continue
        for img2, is_matching in matches.items():
            if is_matching:
                if y_pred[img1][img2]:
                    true_positive += 1
                else:
                    false_negative += 1
            elif not is_matching:
                if not y_pred[img1][img2]:
                    true_negative += 1
                else:
                    false_positive += 1
    res = {'true_positive': true_positive, 'true_negative': true_negative, 'false_positive': false_positive,
           'false_negative': false_negative}
    return res


def score_folder(folder_path, params, print_matches=False):
    image_paths = sorted([i for i in recursive_ls(folder_path)])
    image_pairs = get_all_pairs(image_paths)
    image_comparer = ImageComparer(params)
    matches = defaultdict(dict)
    for img1_path, img2_path in image_pairs:
        img1 = MyImage(img1_path, params)
        img2 = MyImage(img2_path, params)
        is_matching = image_comparer.compare_images(img1, img2, print_matches)
        matches[os.path.basename(img1.path)][os.path.basename(img2_path)] = is_matching
    # print(f"Found {list(matches.values()).count(True)} matches out of total {len(image_pairs)} pairs")
    return matches
