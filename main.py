import streamlit as st
from streamlit_option_menu import option_menu
from src.data_loader import load_data, load_saved_file, init_session_state, list_saved_files
from src.data_processor import process_data
from src.data_visualization import visualize_data
from src.feature_engineering import feature_engineering

# Set page config at the very beginning
st.set_page_config(page_title="NeatPlot", page_icon="📈", layout="wide")

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background-color: #f8fafc;
        padding: 2rem;
    }
    
    h1 {
        color: #1e40af;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    h2 {
        color: #1e40af;
        font-weight: 600;
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    
    h3 {
        color: #3b82f6;
        font-weight: 500;
        font-size: 1.4rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    .stButton>button {
        background-color: #3b82f6;
        color: white;
        font-weight: 500;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #2563eb;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .stRadio>div {
        background-color: #e0f2fe;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
    }
    
    .stSuccess, .stWarning, .stInfo {
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 1rem;
    }
    
    .stSuccess {
        background-color: #d1fae5;
        color: #065f46;
        border-left: 5px solid #059669;
    }
    
    .stWarning {
        background-color: #fef3c7;
        color: #92400e;
        border-left: 5px solid #d97706;
    }
    
    .stInfo {
        background-color: #dbeafe;
        color: #1e40af;
        border-left: 5px solid #3b82f6;
    }
    
    .css-1v0mbdj.etr89bj1 {
        border-radius: 8px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        overflow: hidden;
    }
    
    .sidebar .sidebar-content {
        background-color: #f0f9ff;
    }
            
    /* Footer Styles */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f8fafc;
        color: #4b5563;
        text-align: center;
        padding: 1rem 0;
        font-size: 0.875rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
init_session_state()

# Sidebar navigation with option_menu
with st.sidebar:
    st.markdown("<h1 style='color: #1e40af; font-size: 2rem;'>📈 NeatPlot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #3b82f6; font-size: 1.2rem;'>Your Data Science Companion</p>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["Getting Data", "Processing Data", "Visualise Data", "Feature Engineering  (Work in Progress)"],
        icons=['cloud-upload', 'list-task', 'bar-chart-fill', 'gear'],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "20px", "background-color": "#f0f9ff", "border-radius": "10px"},
            "icon": {"color": "#1e40af", "font-size": "20px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "0px",
                "--hover-color": "#bfdbfe",
                "padding": "15px",
                "border-radius": "7px",
            },
            "nav-link-selected": {"background-color": "#3b82f6", "color": "white", "font-weight": "600"},
        }
    )    
# Main app logic
def main():
    st.markdown("<h1 style='text-align: center; color: #1e40af;'>📈 NeatPlot</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #3b82f6; font-size: 1.2rem;'>Your all-in-one solution for data science workflows</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border: 2px solid #3b82f6; border-radius: 5px; margin-bottom: 2rem;'>", unsafe_allow_html=True)

    if selected == "Getting Data":
        st.header("📂 Data Loading")
        
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Choose data source")
            data_source = st.radio("", ["Upload New File", "Load Saved File"])
        
        with col2:
            # st.subheader("Data Loading")
            if data_source == "Upload New File":
                st.session_state.data = load_data()
            else:
                st.session_state.data = load_saved_file()
        
        if st.session_state.data is not None:
            st.success("✅ Data loaded successfully!")
            st.subheader("Preview of loaded data")
            st.dataframe(st.session_state.data.head(), use_container_width=True)

    elif selected == "Processing Data":
        st.header("🔧 Data Preprocessing")
        if st.session_state.data is not None:
            st.session_state.data = process_data(st.session_state.data)
            # st.success("✅ Data processed successfully!")
            st.subheader("Preview of processed data")
            st.dataframe(st.session_state.data.head(), use_container_width=True)
        else:
            st.warning("Please load data first.")

    elif selected == "Visualise Data":
        st.header("📊 Data Visualization")
        if st.session_state.data is not None:
            visualize_data(st.session_state.data)
        else:
            st.warning("Please load and process data first.")

    elif selected == "Feature Engineering  (Work in Progress)":
        feature_engineering(st.session_state.data)



# Footer
    st.markdown(
        """
        <div class="footer">
            Made with 🖤 by Akhil Sam Varghese
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()