import os
import shutil

import cv2
from common.gridsearch import SiftGridSearch
from common.utils import recursive_ls, get_all_pairs, convert_webp_to_jpg
from common.image_resizer import ImageResizer
from collections import defaultdict
import time


def preprocess_images():
    images = recursive_ls('./data/images/')
    for idx, image in enumerate(images):
        # rename the image to folder name
        os.rename(image, os.path.dirname(image) + str(idx) + '.' + image.split('.')[-1])
        # convert to jpg format
        if image.split('.')[-1] == 'webp':
            convert_webp_to_jpg(image, image.replace('.webp', '.jpg'))
            os.remove(image)
        # fix big ben
        os.rename(image, image.replace('big_ben/images', 'big_ben/big_ben'))
        # copy everything to mixed
        shutil.copy(image, './data/images/mixed/')


def create_dataset(input_path, output_path, size):
    for path in os.listdir(input_path):
        image_resizer = ImageResizer(os.path.join(input_path, path), f'{output_path}/{size[0]}x{size[1]}')
        image_resizer.resize_images(size)


def get_matching(img_1, img_2):
    file_name = img_1.split('/')[-1]
    first_part_of_string = file_name.split('_')[0]
    other_file_name = img_2.split('/')[-1]
    other_first_part_of_string = other_file_name.split('_')[0]
    if first_part_of_string == other_first_part_of_string and first_part_of_string != 'non':
        return True
    return False


def create_matrix(folder_path):
    image_paths = sorted(recursive_ls(folder_path))
    image_pairs = get_all_pairs(image_paths)
    matches = defaultdict(dict)
    for img1_path, img2_path in image_pairs:
        is_matching = get_matching(img1_path, img2_path)
        matches[os.path.basename(img1_path)][os.path.basename(img2_path)] = is_matching
    return matches


if __name__ == '__main__':
    input_path = '/Users/shayarbiv/Downloads/v2/agg3'
    y_test = create_matrix(input_path)
    # y_pred = score_folder("./data/v2/all/")
    grid = {
        'threshold': [19, 21, 22],
        'matcher': [cv2.BFMatcher()],
        'nfeatures': [3600, 4800],
        'n_octave_layers': [None],
        'contrast_threshold': [None],
        'edge_threshold': [3000, 4000, 5000],
        'sigma': [None]
    }

    grid_search = SiftGridSearch(input_path, grid,
                                 f'/Users/shayarbiv/Downloads/v2/agg3/grid_results_{time.time()}.csv', y_test)
    grid_search.run()

# create_dataset('./data/images/original', './data/images/', (640, 480))

# image_converter = ImageConverter('./data/images/original/statue_of_liberty',
#                                  './data/images/original/statue_of_liberty', 'jpg', 'jpeg')
# image_converter.convert_images()
