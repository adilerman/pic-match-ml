import glob
import os

import cv2
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from common.utils import remove_files_in_folder
from pyscripts.image_classifier import ImageClassifier


def save_test_image(img):
    if type(img) == str:
        img = cv2.imread(img)
    else:
        image_pil = Image.open(img)
        img = np.array(image_pil)
    remove_files_in_folder('./data/test_data/')
    cv2.imwrite(f"./data/test_data/test_img.jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))


def classify_image(bg_image):
    save_test_image(bg_image)
    test_image_path = os.path.abspath("./data/test_data/test_img.jpg")
    labeled_images_path = os.path.abspath("./data/labeled_data/")
    image_classifier = ImageClassifier(labeled_images_path)
    pred = image_classifier.classify(test_image_path)
    return pred


if __name__ == '__main__':
    try:
        st.set_page_config(page_title="Image Classifier", layout='wide')
        st.title('Image Classifier')
        task = st.radio("Select classification task", ["Single image", "Classifications by path"])
        if task == "Single image":
            bg_image = st.file_uploader("Teat image to classify:", type=["png", "jpg"])
            if bg_image:
                pred = classify_image(bg_image)
                st.success(f"The image contains the object" if pred == 'b' else "The image does not contain the object")
        if task == "Classifications by path":
            predictions = []
            test_images_path = st.text_input("Path to classify")
            if test_images_path:
                test_images_path += '/' if test_images_path[-1] != '/' else ''
                images_to_classify_path = glob.glob(test_images_path + '*.j*')
                submit_clicked = st.button('Submit')
                if submit_clicked:
                    for image_to_classify in images_to_classify_path:
                        pred = classify_image(image_to_classify)
                        predictions.append([image_to_classify, pred])
                    st.dataframe(pd.DataFrame(predictions))
    except Exception as e:
        print(e)
        st.write(e)
