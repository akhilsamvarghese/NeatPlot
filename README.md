# NeatPlot: Your Data Science Companion
![NeatPlot Image](https://drive.google.com/uc?id=1G32R1641cvkd164I19ftM3GDtFv86b5g)


## Overview

NeatPlot is an all-in-one solution for data science workflows, providing a user-friendly interface for data loading, processing, visualization, and feature engineering. Built with Streamlit, this application offers a seamless experience for data scientists and analysts to explore and manipulate their datasets.

## Features

- **Data Loading**: 
  - Upload new CSV files
  - Load previously saved files
  - Automatic encoding detection for CSV files

- **Data Processing**:
  - Select specific columns for analysis
  - Handle missing values (drop or fill)
  - Convert data types
  - Remove special characters from string columns

- **Data Visualization**:
  - Univariate Analysis:
    - Summary Statistics
    - Histograms
    - Box Plots
    - Violin Plots
    - Bar Charts
  - Bivariate Analysis:
    - Scatter Plots
    - Correlation Heatmaps
    - Group Box Plots
    - Bar Charts
  - 3D Scatter Plots

- **Feature Engineering** (Coming Soon):
  - Placeholder for future feature engineering capabilities

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/neatplot.git
   cd neatplot
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run main.py
   ```

2. Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

3. Use the sidebar to navigate between different sections of the application:
   - Getting Data
   - Processing Data
   - Visualise Data
   - Feature Engineering

4. Follow the on-screen instructions in each section to load, process, and visualize your data.

## Project Structure

- `main.py`: The main Streamlit application file
- `src/`:
  - `data_loader.py`: Functions for loading and saving data
  - `data_processor.py`: Functions for data preprocessing
  - `data_visualization.py`: Functions for data visualization
- `saved_files/`: Directory for storing uploaded and saved CSV files
- `cleaned_data/`: Directory for storing processed and cleaned data files

## Contributing

Contributions to NeatPlot are welcome! Please feel free to submit a Pull Request.
