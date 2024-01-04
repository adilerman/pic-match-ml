import streamlit as st

if __name__ == '__main__':
    st.set_page_config(page_title='Pic-Match ML', layout='wide', page_icon='🏠')
    st.sidebar.header("Tool for image manipulation and detection.")
    st.title("Welcome to Pic-Match ML")
    st.image('./data/home_bg.jpeg', width=600)
