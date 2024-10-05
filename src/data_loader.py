import streamlit as st
import pandas as pd
import os
from datetime import datetime

UPLOAD_DIRECTORY = "saved_files"

def load_data():
    st.subheader("Data Loading")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    if uploaded_file is not None:
        # Read the CSV file
        data = pd.read_csv(uploaded_file)
        
        # Display the first few rows of the data
        st.write("Preview of the data:")
        st.write(data.head())
        
        # Column selection
        data = select_columns(data)
        
        # Option to save the uploaded file
        if st.button("Save Uploaded File"):
            saved_filename = save_uploaded_file(data)
            st.session_state.uploaded_files.append(saved_filename)
        
        return data
    
    return None

def save_uploaded_file(data):
    # Create a 'saved_files' directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    
    # Generate a unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"uploaded_file_{timestamp}.csv"
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    
    # Save the file
    data.to_csv(file_path, index=False)
    
    st.success(f"File saved as {file_name}")
    return file_name

def load_saved_file():
    st.subheader("Load Saved File")

    # Get list of saved files
    saved_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith('.csv')]

    if not saved_files:
        st.warning("No saved files found.")
        return None


    # Let user select a file
    selected_file = st.selectbox("Choose a file to load", saved_files)

    if selected_file:
        file_path = os.path.join(UPLOAD_DIRECTORY, selected_file)
        data = pd.read_csv(file_path)

        # Display the first few rows of the data
        st.write("Preview of the data:")
        st.write(data.head())   
        
        # Column selection
        data = select_columns(data)
        
        return data

    return None

def select_columns(df):
    st.subheader("Select Columns")
    
    select_all = ["Select All"]
    full_columns = select_all + df.columns.tolist()
    
    columns = st.multiselect("Select the columns", full_columns)
    
    if "Select All" in columns or not columns:
        selected_df = df
    else:
        selected_df = df[columns]
    
    # Display the DataFrame
    st.write("Preview of selected data:")
    st.dataframe(selected_df.head(), use_container_width=True)
    
    return selected_df

# Initialize session state
def init_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

# Function to list saved files
def list_saved_files():
    saved_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith('.csv')]
    return saved_files