import streamlit as st
import pandas as pd
import os
from datetime import datetime
import chardet
import json
import openpyxl

UPLOAD_DIRECTORY = "saved_files"

def load_data():
    st.subheader("Data Loading")

    # File uploader
    uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx", "xls", "json"])
    
    if uploaded_file is not None:
        try:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            
            if file_extension == '.csv':
                data = load_csv(uploaded_file)
            elif file_extension in ['.xlsx', '.xls']:
                data = load_excel(uploaded_file)
            elif file_extension == '.json':
                data = load_json(uploaded_file)
            else:
                st.error(f"Unsupported file type: {file_extension}")
                return None
            
            # Display the first few rows of the data
            st.write("Preview of the data:")
            st.write(data.head())
            
            # Option to save the uploaded file
            if st.button("Save Uploaded File"):
                saved_filename = save_uploaded_file(data, file_extension)
                st.session_state.uploaded_files.append(saved_filename)
            
            return data
        
        except Exception as e:
            st.error(f"An error occurred while loading the file: {str(e)}")
    
    return None

def load_csv(file):
    # Detect the file encoding
    raw_data = file.read()
    detected_encoding = chardet.detect(raw_data)['encoding']
    
    # Reset the file pointer to the beginning
    file.seek(0)
    
    # Try to read the CSV file with the detected encoding
    return pd.read_csv(file, encoding=detected_encoding)

def load_excel(file):
    return pd.read_excel(file)

def load_json(file):
    json_data = json.load(file)
    return pd.json_normalize(json_data)

def save_uploaded_file(data, file_extension):
    # Create a 'saved_files' directory if it doesn't exist
    if not os.path.exists(UPLOAD_DIRECTORY):
        os.makedirs(UPLOAD_DIRECTORY)
    
    # Generate a unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"uploaded_file_{timestamp}{file_extension}"
    file_path = os.path.join(UPLOAD_DIRECTORY, file_name)
    
    # Save the file based on its extension
    if file_extension == '.csv':
        data.to_csv(file_path, index=False)
    elif file_extension in ['.xlsx', '.xls']:
        data.to_excel(file_path, index=False)
    elif file_extension == '.json':
        data.to_json(file_path, orient='records')
    
    st.success(f"File saved as {file_name}")
    return file_name

def load_saved_file():
    st.subheader("Load Saved File")

    # Get list of saved files
    saved_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith(('.csv', '.xlsx', '.xls', '.json'))]

    if not saved_files:
        st.warning("No saved files found.")
        return None

    # Let user select a file
    selected_file = st.selectbox("Choose a file to load", saved_files)

    if selected_file:
        file_path = os.path.join(UPLOAD_DIRECTORY, selected_file)
        file_extension = os.path.splitext(selected_file)[1].lower()

        try:
            if file_extension == '.csv':
                data = pd.read_csv(file_path)
            elif file_extension in ['.xlsx', '.xls']:
                data = pd.read_excel(file_path)
            elif file_extension == '.json':
                with open(file_path, 'r') as json_file:
                    json_data = json.load(json_file)
                data = pd.json_normalize(json_data)
            else:
                st.error(f"Unsupported file type: {file_extension}")
                return None

            # Display the first few rows of the data
            st.write("Preview of the data:")
            st.write(data.head())
            
            return data
        except Exception as e:
            st.error(f"An error occurred while loading the file: {str(e)}")

    return None

# Initialize session state
def init_session_state():
    if 'data' not in st.session_state:
        st.session_state.data = None
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

# Function to list saved files
def list_saved_files():
    saved_files = [f for f in os.listdir(UPLOAD_DIRECTORY) if f.endswith(('.csv', '.xlsx', '.xls', '.json'))]
    return saved_files