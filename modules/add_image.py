# Author: Mike Allen 25119947
import streamlit as st
import PIL.Image as Image

def insert_image():
    # Adding an image and file upload section
    st.sidebar.markdown("<style>'div.block-container{'padding:1rem;'}</style>", unsafe_allow_html=True)
    image = Image.open('images/ecomove_AI.jpeg')
    left_co, cent_co,last_co = st.sidebar.columns([1,3,1])
    with cent_co:
        st.sidebar.image(image, width=180)