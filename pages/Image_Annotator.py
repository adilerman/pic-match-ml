import os
import cv2
import numpy as np

import pandas as pd
from PIL import Image, ImageDraw
import streamlit as st
from streamlit_drawable_canvas import st_canvas


def draw_bounding_box(image, box):
    # Draw bounding box on the image
    draw = ImageDraw.Draw(image)
    draw.rectangle(box, outline="red", width=3)
    return image


def draw_canvas(bg_image):
    return st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=1,
        stroke_color='#000000',
        background_color='#eee',
        background_image=Image.open(bg_image),
        height=Image.open(bg_image).size[1],
        width=Image.open(bg_image).size[0],
        drawing_mode="rect",
        point_display_radius=0,
        key="canvas",
    )


def get_bounding_box(canvas_result, bg_image):
    objects = pd.json_normalize(canvas_result.json_data["objects"])  # need to convert obj to str because PyArrow
    for col in objects.select_dtypes(include=['object']).columns:
        objects[col] = objects[col].astype("str")
        # x,y : lower left corner
    # x2,y2 : upper right corner
    x, y, x2, y2 = [objects.iloc[-1]['left'], Image.open(bg_image).size[1] - objects.iloc[-1]['top'] - objects.iloc[-1]['height'],
                    objects.iloc[-1]['left'] + objects.iloc[-1]['width'],
                    Image.open(bg_image).size[1] - objects.iloc[-1]['top']]
    return x, y, x2, y2


def save_label(img, x, y, x2, y2, label):
    # Count the number of files
    num_files = int((len(os.listdir(f'./data/labeled_data/')) / 2) + 1)
    file_name = f'{label}_{num_files}'
    f = open(f'./data/labeled_data/{file_name}.bb', 'w')
    f.write(f"{x}_{y}_{x2}_{y2}")
    f.close()
    cv2.imwrite(f"./data/labeled_data/{file_name}.jpg", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    st.warning(f"Label Saved to path {file_name}")


def reset_state():
    st.session_state.selected_class = None


try:
    st.set_page_config(page_title="Image Annotator", layout='wide')
    st.title('Image Annotator')
    bg_image = st.file_uploader("Background image:", type=["png", "jpg"])
    # print(bg_image)
    if bg_image:
        image_pil = Image.open(bg_image)
        img_np = np.array(image_pil)
        canvas_result = draw_canvas(bg_image)
        # Do something interesting with the image data and paths
        if canvas_result.json_data and canvas_result.json_data.get('objects'):
            # Initialize session state if it doesn't exist
            if "selected_class" not in st.session_state:
                reset_state()
            x, y, x2, y2 = get_bounding_box(canvas_result, bg_image)
            col1, col2 = st.columns(2)
            if col1.button("Object Located"):
                st.session_state.selected_class = 'class_b'
            if col2.button("No Object"):
                st.session_state.selected_class = 'class_a'

            if st.session_state.selected_class:
                st.session_state.save_label_button = st.button('Save Label')
                if st.session_state.save_label_button:
                    save_label(img_np, x, y, x2, y2, label=st.session_state.selected_class)
                    reset_state()
except Exception as e:
    print(e)
    st.write(e)
