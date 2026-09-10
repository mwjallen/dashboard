# Author: Mike Allen 25119947
import streamlit as st
import pandas as pd

def file_upload():
    """
    Upload a CSV or Excel file and store it in the session state.

    Returns:
        None
    """
    st.sidebar.divider()
    st.sidebar.header('File Upload')
    uploaded_file = st.sidebar.file_uploader('File type csv or xlsx only',type=['csv', 'xlsx'])
    st.sidebar.divider()

    if uploaded_file:
        if uploaded_file.name.endswith('.csv'):
            df=pd.read_csv(uploaded_file)
        else:
            df=pd.read_excel(uploaded_file)
    else:
        df = pd.read_excel('cleaned_ds.xlsx')
        st.session_state['dataframe'] = df