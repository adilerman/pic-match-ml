import streamlit as st
import glob
import os
import cv2
from stqdm import stqdm
import pandas as pd

from pyscripts.my_image import MyImage


class StereoSplitter:
    def __init__(self, img: MyImage):
        self.matcher = cv2.BFMatcher_create()
        self.img = img

    def is_stereo_image(self):
        matches = self.find_matches(self.img, self.img)
        return matches

    def find_matches(self, img1, img2):
        matches = self.matcher.knnMatch(img1.descriptors, img2.descriptors, k=3)
        good_matches = []
        for n_1, n_2, n_3 in matches:
            if (img2.keypoints[n_1.trainIdx] == img1.keypoints[n_1.queryIdx]) and \
                    ((1.1 * img2.keypoints[n_2.trainIdx].pt[1] > img1.keypoints[n_2.queryIdx].pt[1]) and
                     (img1.keypoints[n_2.queryIdx].pt[1] > 0.9 * img2.keypoints[n_2.trainIdx].pt[1])) and \
                    n_3.distance > 1.28 * n_2.distance:
                good_matches.append(n_2)
        return good_matches


def run_image(image_path):
    image_obj = MyImage(image_path)
    stereo_splitter = StereoSplitter(image_obj)
    image_inner_matches = stereo_splitter.is_stereo_image()
    if len(image_inner_matches) > 410:
        return True
    return False


def detect(path):
    y_pred = []
    if os.path.isdir(path):
        image_list = glob.glob(os.path.join(path, '*'))
        for image_path in stqdm(image_list):
            stereo = run_image(image_path)
            if stereo:
                y_pred.append(image_path)
    else:
        run_image(path)
    st.session_state.y_pred = y_pred
    return


st.set_page_config(page_title="Stereo Images Detector", layout='wide')
st.title('Stereo Images Detector')
path = st.text_input("Enter images folder path", key=f'stereo_detector_output_path')
if path:
    submit_clicked = st.button('Submit', on_click=detect, kwargs={'path': path})
    if submit_clicked:
        df = pd.DataFrame(st.session_state.y_pred, columns=['stereo_images'])
        st.dataframe(df)
        st.caption(f'Total Images Found: {len(df.index)}')
