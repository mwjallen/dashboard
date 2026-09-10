# Author: Mike Allen 25119947
import streamlit as st
# To show the browser window scrollbar
def show_scrollbar():
    st.markdown(
        """
        <style>
        ::-webkit-scrollbar {
            width: 12px;
        }
        ::-webkit-scrollbar-thumb {
            background: #888;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #555;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
