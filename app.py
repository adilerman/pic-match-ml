import streamlit as st

from classifier import classifier
from labeler import labeler
from stereo_depth_mapper import stereo_depth_mapper


def intro():
    pass


if __name__ == '__main__':
    page_names_to_funcs = {
        "—": intro,
        "Label data": labeler,
        "Classify images": classifier,
        "Detect stereo images": stereo_depth_mapper
    }
    st.sidebar.title("Welcome to pic match ml")
    st.sidebar.subheader(
        "This tool for image manipulation and detection.")

    demo_name = st.sidebar.selectbox("Choose a UI", page_names_to_funcs.keys())
    page_names_to_funcs[demo_name]()

