import datetime
import os
import shutil
import caffeine
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
        shutil.copy(image, 'data/images/mixed/')


def create_dataset(input_path, output_path, size):
    image_resizer = ImageResizer(input_path, f'{output_path}/{size[0]}x{size[1]}')
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
    input_path = '/Users/adilerman/Downloads/images/real'
    y_test = create_matrix(input_path)
    start = datetime.datetime.now()
    print(f'{datetime.datetime.now() - start}0')
    # grid = {
    #     'threshold': [20, 21, 22],
    #     'matcher': [cv2.BFMatcher],
    #     'nfeatures': [0, 1000, 3000, 6000],
    #     'n_octave_layers': [None, 2, 3],
    #     'contrast_threshold': [0.09, 0.02, 0.03],
    #     'edge_threshold': [5, 10, 15],
    #     'sigma': [1.0, 1.6, 2.0]
    # }
    grid = {
        'threshold': [22],
        'matcher': [cv2.BFMatcher],
        'nfeatures': [3000],
        'n_octave_layers': [ 3],
        'contrast_threshold': [0.09],
        'edge_threshold': [ 10],
        'sigma': [ 1.6]
    }
    print(f'{datetime.datetime.now() - start}t0')
    grid_search = SiftGridSearch(input_path, grid, f'./original_1024_gan_grid_results_{time.time()}.csv', y_test)
    print(f'{datetime.datetime.now() - start}t1')
    grid_search.run()
    print(f'{datetime.datetime.now() - start} end')