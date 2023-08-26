import os
import itertools


def filter_nested_lists(nested_list, result=[]):
    for item in nested_list:
        if isinstance(item, list):
            filter_nested_lists(item, result)
        else:
            result.append(nested_list)
            break
    return result


def recursive_ls(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        # Append all files in the current directory to the list
        for file in files:
            file_list.append(os.path.join(root, file))

    return file_list


def get_all_pairs(lst):
    return list(itertools.combinations(lst, 2))


def convert_webp_to_jpg(webp_path, jpg_path):
    # Open the WebP image
    image = Image.open(webp_path)
    # Convert to RGB if the image mode is not 'RGB'
    if image.mode != "RGB":
        image = image.convert("RGB")
    # Save as JPG
    image.save(jpg_path, "JPEG")
