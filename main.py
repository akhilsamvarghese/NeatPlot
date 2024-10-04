import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Set page config at the very beginning
st.set_page_config(page_title="Data Science App", page_icon="🧊", layout="wide")

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
        
        # Option to save the uploaded file
        if st.button("Save Uploaded File"):
            save_uploaded_file(uploaded_file)
        
        # Column selection for custom DataFrame
        st.subheader("Create Custom DataFrame")
        selected_columns = st.multiselect("Select columns for your custom DataFrame", data.columns.tolist())
        
        if selected_columns:
            custom_df = data[selected_columns]
            st.write("Preview of your custom DataFrame:")
            st.write(custom_df.head())
            return custom_df
        
        return data
    
    return None

def save_uploaded_file(uploadedfile):
    # Create a 'saved_files' directory if it doesn't exist
    if not os.path.exists("saved_files"):
        os.makedirs("saved_files")
    
    # Generate a unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"saved_files/uploaded_file_{timestamp}.csv"
    
    # Save the file
    with open(file_name, "wb") as f:
        f.write(uploadedfile.getbuffer())
    
    st.success(f"File saved as {file_name}")

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Getting Data", "Processing Data", "Visualise Data", "Feature Engineering"])

# Main app logic
def main():
    if page == "Getting Data":
        st.title("Data Loading")
        st.session_state.data = load_data()
        if st.session_state.data is not None:
            st.success("Data loaded successfully!")

    elif page == "Processing Data":
        st.title("Data Processing")
        if st.session_state.data is not None:
            # Add your data processing logic here
            st.write(st.session_state.data.head())
        else:
            st.warning("Please load data first.")

    elif page == "Visualise Data":
        st.title("Data Visualization")
        if st.session_state.data is not None:
            # Add your data visualization logic here
            st.write("Visualization placeholder")
        else:
            st.warning("Please load and process data first.")

    elif page == "Feature Engineering":
        st.title("Feature Engineering")
        if st.session_state.data is not None:
            # Add your feature engineering logic here
            st.write(st.session_state.data.head())
        else:
            st.warning("Please load and process data first.")

if __name__ == "__main__":
    main()