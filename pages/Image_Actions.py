import streamlit as st
from tempfile import TemporaryDirectory
import os
import time

from common.images import trim_borders, vertical_split, combo_trim_split

FUNC_MAP = {
        'trim_borders': trim_borders,
        'vertical_split': vertical_split,
        'trim_&_split_combo': combo_trim_split
    }


def save_uploaded_file(temp_dir, uploaded_file):
    with open(os.path.join(temp_dir, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return st.success(f'Saved results in output folder')


def image_file_uploads(key):
    image_files = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"], accept_multiple_files=True,
                                   key=f'{key}_file_upload')
    output_path = st.text_input("Enter output path for images", key=f'{key}_output_path', value=None)
    return image_files, output_path


# def disable_submit():
#     st.session_state.submit_disabled = True


def main():
    st.set_page_config(page_title="Image actions", layout='wide')
    st.title('Image actions')

    action = st.radio("Choose the action you want", ['Trim Borders', 'Vertical Split', 'Trim & Split Combo'],
                      index=None, horizontal=True, key='action_radio')

    # if 'submit_disabled' not in st.session_state:
    #     st.session_state.submit_disabled = False

    if st.session_state.action_radio:
        action = action.lower().replace(" ", "_")
        files, output_path = image_file_uploads(action)
        if files and output_path:
            do_action = st.button('Submit', key=f'{action}_submit')
            for file in files:
                _, file_ext = os.path.splitext(file.name)
                if do_action:
                    with TemporaryDirectory() as temp_dir:
                        temp_file_name = file.name
                        temp_file_path = os.path.join(temp_dir, temp_file_name)
                        save_uploaded_file(temp_dir, file)
                        FUNC_MAP[action](temp_file_path, output_path, None)

        # st.rerun()  #TODO add st.empty() for showing the images


if __name__ == '__main__':
    main()

