import json

import requests
import streamlit as st

from common.utils import streamlit_image_to_cv2, image_to_mask, numpy_to_base64_url, base64_url_to_image


def get_depth_map_from_api(base64_url1, base64_url2):
    payload = json.dumps({"data": [base64_url1, base64_url2, 'stereo']})
    response = requests.request("POST", url='https://haofeixu-unimatch.hf.space/run/predict',
                                headers={'Content-Type': 'application/json'}, data=payload)
    return base64_url_to_image(response.json()['data'][0])


def stereo_depth_mapper():
    st.success("Upload 2 parts of the stereo images")
    # Upload the first image
    images = st.file_uploader("Upload the first image", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    if len(images) == 2:
        run = st.button("Create depth map")
        if run:
            img1, img2 = images
            mask1 = image_to_mask(streamlit_image_to_cv2(img1))
            mask2 = image_to_mask(streamlit_image_to_cv2(img2))
            base64_url1 = numpy_to_base64_url(mask1)
            base64_url2 = numpy_to_base64_url(mask2)
            depth_map = get_depth_map_from_api(base64_url1, base64_url2)
            st.image(depth_map, caption='Depth map', use_column_width=True)
