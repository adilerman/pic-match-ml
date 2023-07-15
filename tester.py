import os
import shutil
from PIL import Image
from image_comparer import ImageComparer
from my_image import MyImage

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


def resize_images(image_paths, size, output_path):
    for image_path in image_paths:
        image = Image.open(image_path)
        resized_image = image.resize(size)
        folder_name = image_path.split('/')[-2]
        os.makedirs(output_path + 'smaller/', exist_ok=True)

        resized_image.save(output_path + 'smaller/' + os.path.basename(image_path))


def score_folder(folder_path):
    image_paths = recursive_ls(folder_path)
    image_pairs = get_all_pairs(image_paths)
    image_comparer = ImageComparer()
    matches = []
    for img1_path, img2_path in image_pairs:
        img1 = MyImage(img1_path)
        img2 = MyImage(img2_path)
        is_matching = image_comparer.compare_images(img1, img2)
        matches.append(is_matching)

    print(f"Found {matches.count(True)} matches out of total {len(image_pairs)} pairs")


def get_all_pairs(lst):
    return list(itertools.combinations(lst, 2))


#
# score_folder('./data/images/smaller/')
image_paths = recursive_ls('./data/images/eiffel')

resize_images(image_paths, size=(256, 256), output_path='data/images/256x256/eiffel/')
