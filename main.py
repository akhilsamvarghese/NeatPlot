import streamlit as st
from src.data_loader import load_data
from src.data_processor import process_data
from src.data_visualization import visualize_data
from src.feature_engineering import custom_feature_engineering

st.set_page_config(page_title="Data Science App", page_icon="🧊", layout="wide")

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Getting Data", "Processing Data", "Visualise Data", "Feature Engineering"])

if page == "Getting Data":
    st.title("Data Loading")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.session_state.data = load_data(uploaded_file)
        st.write(st.session_state.data.head())

elif page == "Processing Data":
    st.title("Data Processing")
    if st.session_state.data is not None:
        st.session_state.data = process_data(st.session_state.data)
        st.write(st.session_state.data.head())
    else:
        st.warning("Please load data first.")

elif page == "Visualise Data":
    st.title("Data Visualization")
    if st.session_state.data is not None:
        visualize_data(st.session_state.data)
    else:
        st.warning("Please load and process data first.")

elif page == "Feature Engineering":
    st.title("Feature Engineering")
    if st.session_state.data is not None:
        st.session_state.data = custom_feature_engineering(st.session_state.data)
        st.write(st.session_state.data.head())
    else:
        st.warning("Please load and process data first.")