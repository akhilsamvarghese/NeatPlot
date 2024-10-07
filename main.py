import streamlit as st
from streamlit_option_menu import option_menu
from src.data_loader import load_data, load_saved_file, init_session_state, list_saved_files
from src.data_processor import process_data

# Set page config at the very beginning
st.set_page_config(page_title="NeatPlot", page_icon="📊", layout="wide")

# Initialize session state
init_session_state()

# Sidebar navigation with option_menu
with st.sidebar:
    st.title("Navigation")
    selected = option_menu(
        menu_title=None,
        options=["Getting Data", "Processing Data", "Visualise Data", "Feature Engineering"],
        icons=['cloud-upload', 'list-task', 'bar-chart-fill', 'gear'],
        menu_icon="cast",
        default_index=0,
    )

# Common header function
def display_header():
    st.title("NeatPlot")
    st.markdown("*Your all-in-one solution for data science workflows*")
    st.markdown("---")

# Main app logic
def main():
    # Display the common header
    display_header()

    if selected == "Getting Data":
        st.header("Data Loading")
        # Option to upload new file or load saved file
        data_source = st.radio("Choose data source", ["Upload New File", "Load Saved File"])
        if data_source == "Upload New File":
            st.session_state.data = load_data()
        else:
            # List saved files
            saved_files = list_saved_files()
            if saved_files:
                st.write("Saved CSV files:")
                for file in saved_files:
                    st.write(f"- {file}")
                st.session_state.data = load_saved_file()
            else:
                st.warning("No saved files found.")
        if st.session_state.data is not None:
            st.success("Data loaded successfully!")

    elif selected == "Processing Data":
        st.header("Data Preprocessing")
        if st.session_state.data is not None:
            st.session_state.data = process_data(st.session_state.data)
        else:
            st.warning("Please load data first.")

    elif selected == "Visualise Data":
        st.header("Data Visualization")
        if st.session_state.data is not None:
            # Add your data visualization logic here
            st.write("Visualization placeholder")
        else:
            st.warning("Please load and process data first.")

    elif selected == "Feature Engineering":
        st.header("Feature Engineering")
        if st.session_state.data is not None:
            # Add your feature engineering logic here
            st.write(st.session_state.data.head())
        else:
            st.warning("Please load and process data first.")

if __name__ == "__main__":
    main()