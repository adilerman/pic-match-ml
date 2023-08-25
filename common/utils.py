def filter_nested_lists(nested_list, result=[]):
    for item in nested_list:
        if isinstance(item, list):
            filter_nested_lists(item, result)
        else:
            result.append(nested_list)
            break
    return result


import os


def rename_files_in_folder(folder_path, base_name):
    # # Example usage
    # folder_path = "/Users/adilerman/PycharmProjects/pic-match-ml/data/old_scraped/agg4"
    # base_name = "agg4"
    # rename_files_in_folder(folder_path, base_name)

    try:
        # Get a list of all files in the folder
        files = os.listdir(folder_path)
        # Sort the list to ensure consistent order
        files.sort()
        for index, old_filename in enumerate(files, start=1):
            # Split the old filename into name and extension
            filename, old_extension = os.path.splitext(old_filename)

            # Construct the new filename with running index and old extension
            new_filename = f"{base_name}_{index}{old_extension}"

            # Create full old and new file paths
            old_file_path = os.path.join(folder_path, old_filename)
            new_file_path = os.path.join(folder_path, new_filename)

            # Rename the file
            os.rename(old_file_path, new_file_path)
            print(f"File '{old_filename}' renamed to '{new_filename}' successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")


import os
import cv2
from my_image import MyImage

import glob


def folder_to_grey(input_path, output_path=None):
    if not output_path:
        output_path = input_path
    if input_path[-1] != '/':
        input_path = input_path + '/'
    if output_path[-1] != '/':
        output_path = output_path + '/'
    files = glob.glob(f"{input_path}*.jpg")
    for file in files:
        file_name = os.path.basename(file)
        print(file_name)
        img = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        cv2.imwrite(f'{output_path}{file_name}', img)


folder_to_grey('/Users/adilerman/PycharmProjects/pic-match-ml/data/v2/non_matching')
