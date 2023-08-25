import os
import shutil
from PIL import Image
from image_comparer import ImageComparer
from my_image import MyImage
from common.image_resizer import ImageResizer
from common.convert_image_format import ImageConverter
from collections import defaultdict
import glob

import itertools


def recursive_ls(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        # Append all files in the current directory to the list
        for file in files:
            file_list.append(os.path.join(root, file))

    return file_list


def convert_webp_to_jpg(webp_path, jpg_path):
    # Open the WebP image
    image = Image.open(webp_path)
    # Convert to RGB if the image mode is not 'RGB'
    if image.mode != "RGB":
        image = image.convert("RGB")
    # Save as JPG
    image.save(jpg_path, "JPEG")


# noinspection PyTypeChecker
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


def score_folder(folder_path, print_matches=True):
    image_paths = sorted(recursive_ls(folder_path))
    image_pairs = get_all_pairs(image_paths)
    image_comparer = ImageComparer()
    matches = defaultdict(dict)
    for img1_path, img2_path in image_pairs:
        img1 = MyImage(img1_path)
        img2 = MyImage(img2_path)
        is_matching = image_comparer.compare_images(img1, img2, print_matches)
        matches[os.path.basename(img1.path)][os.path.basename(img2_path)] = is_matching

    print(f"Found {list(matches.values()).count(True)} matches out of total {len(image_pairs)} pairs")
    return matches, image_pairs


def get_all_pairs(lst):
    return list(itertools.combinations(lst, 2))


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

    print(f"Found {list(matches.values()).count(True)} matches out of total {len(image_pairs)} pairs")
    return matches, image_pairs

# score_folder('./data/old_scraped/agg4', print_matches=False)


m, pairs = create_matrix("/Users/shayarbiv/Downloads/test_v2/")

print('hello')
# image_paths = recursive_ls('./data/images/original/')

# create_dataset('./data/images/original', './data/images/', (640, 480))

#
# image_converter = ImageConverter('./data/images/original/statue_of_liberty',
#                                  './data/images/original/statue_of_liberty', 'jpg', 'jpeg')
# image_converter.convert_images()
