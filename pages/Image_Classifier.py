import os

import cv2
import numpy as np
import streamlit as st
from PIL import Image

from common.utils import remove_files_in_folder
from pyscripts.image_classifier import ImageClassifier


def save_test_image(img):
    image_pil = Image.open(img)
    img_np = np.array(image_pil)
    remove_files_in_folder('../data/test_data/')
    cv2.imwrite(f"../data/test_data/test_img.jpg", cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR))


try:
    st.set_page_config(page_title="Image Classifier", layout='wide')
    st.title('Image Classifier')
    bg_image = st.file_uploader("Background image:", type=["png", "jpg"])
    if bg_image:
        save_test_image(bg_image)
        test_image_path = os.path.abspath("../data/test_data/test_img.jpg")
        labeled_images_path = os.path.abspath("../data/labeled_data/")
        image_classifier = ImageClassifier(labeled_images_path)
        pred = image_classifier.classify(test_image_path)
        st.success(f"The image contains the object" if pred == 'b' else "The image does not contain the object")
except Exception as e:
    print(e)
    st.write(e)
