import base64
import os
import itertools
from io import BytesIO

import cv2
from PIL import Image
import numpy as np


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


def remove_files_in_folder(folder_path):
    # Get the list of files in the folder
    file_list = os.listdir(folder_path)

    # Iterate through the files and remove each one
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"File removed: {file_path}")
        except Exception as e:
            print(f"Error removing file {file_path}: {e}")


def streamlit_image_to_cv2(streamlit_image):
    pil_image = Image.open(streamlit_image)
    cv2_image = np.array(pil_image)
    return cv2_image



def base64_url_to_image(base64_url):
    base64_data = base64_url.split(",")[1]
    img_data = base64.b64decode(base64_data)
    img = Image.open(BytesIO(img_data))
    return img


# Function to convert image to mask
def image_to_mask(img):
    _, mask = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)
    return mask


# Function to encode NumPy array as base64 URL
def numpy_to_base64_url(arr):
    img = Image.fromarray(arr)
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    base64_url = "data:image/png;base64," + img_str
    return base64_url

