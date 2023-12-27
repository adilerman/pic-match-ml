import os
import itertools
from PIL import Image


def read_points_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.read().strip()
            points = [int(coord) for coord in data.split('_')]
            if len(points) == 4:
                x1, y1, x2, y2 = points
                return x1, y1, x2, y2
            else:
                print("Error: File does not contain valid points.")
                return None
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def is_point_inside_box(x1, y1, x2, y2, x3, y3):
    """Check if a point (x3, y3)
        is inside a bounding box defined by two points
        (x1, y1) and (x2, y2)"""
    min_x = min(x1, x2)
    max_x = max(x1, x2)
    min_y = min(y1, y2)
    max_y = max(y1, y2)
    if min_x <= x3 <= max_x and min_y <= y3 <= max_y:
        return True
    else:
        return False


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
