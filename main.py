import streamlit as st
from src.data_loader import load_data, init_session_state

# Set page config at the very beginning
st.set_page_config(page_title="Data Science App", page_icon="🧊", layout="wide")

# Initialize session state
init_session_state()

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