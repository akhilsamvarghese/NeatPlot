import streamlit as st
import pandas as pd
import numpy as np

def process_data(df):
    st.subheader("Data Processing")

    option = st.selectbox("Select an option:", [
        "Top 5 Records", "Shape of Data", "Null Values",
        "Duplicates", "Data Types", "Summary Statistics",
        "Unique Values"
    ])

    if option == "Top 5 Records":
        show_top_records(df)
    elif option == "Shape of Data":
        show_data_shape(df)
    elif option == "Null Values":
        handle_null_values(df)
    elif option == "Duplicates":
        handle_duplicates(df)
    elif option == "Data Types":
        handle_datatypes(df)
    elif option == "Summary Statistics":
        show_summary_statistics(df)
    elif option == "Unique Values":
        show_unique_values(df)

    return df

def show_top_records(df):
    st.write("Top 5 Records:")
    st.write(df.head())

def show_data_shape(df):
    st.write(f"Shape of the DataFrame: {df.shape}")
    st.write(f"Number of rows: {df.shape[0]}")
    st.write(f"Number of columns: {df.shape[1]}")

def handle_null_values(df):
    st.write("Null Values:")
    null_counts = df.isnull().sum()
    st.write(null_counts)
    
    if null_counts.sum() > 0:
        st.write("Options to handle null values:")
        null_handling = st.radio("Choose an option:", ["Drop rows with null values", "Fill null values"])
        
        if null_handling == "Drop rows with null values":
            df_cleaned = df.dropna()
            st.write(f"Rows remaining after dropping null values: {len(df_cleaned)}")
        else:
            fill_method = st.selectbox("Choose fill method:", ["Mean", "Median", "Mode", "Custom value"])
            if fill_method == "Custom value":
                fill_value = st.text_input("Enter custom value:")
            else:
                fill_value = None
            
            for column in df.columns[df.isnull().any()]:
                if pd.api.types.is_numeric_dtype(df[column]):
                    if fill_method == "Mean":
                        df[column].fillna(df[column].mean(), inplace=True)
                    elif fill_method == "Median":
                        df[column].fillna(df[column].median(), inplace=True)
                    elif fill_method == "Mode":
                        df[column].fillna(df[column].mode()[0], inplace=True)
                    else:
                        df[column].fillna(fill_value, inplace=True)
                else:
                    if fill_method == "Mode":
                        df[column].fillna(df[column].mode()[0], inplace=True)
                    else:
                        df[column].fillna(fill_value, inplace=True)
        
        st.write("Null values after handling:")
        st.write(df.isnull().sum())

def handle_duplicates(df):
    st.write(f"Number of duplicate rows: {df.duplicated().sum()}")
    if df.duplicated().sum() > 0:
        remove_duplicates = st.checkbox("Remove duplicate rows")
        if remove_duplicates:
            df.drop_duplicates(inplace=True)
            st.write(f"Rows remaining after removing duplicates: {len(df)}")

def handle_datatypes(df):
    st.write("Data Types:")
    st.write(df.dtypes)
    
    columns_to_change = st.multiselect("Select columns to change data type:", df.columns)
    for column in columns_to_change:
        new_type = st.selectbox(f"New data type for {column}:", ["int64", "float64", "object", "datetime64"])
        try:
            if new_type == "datetime64":
                df[column] = pd.to_datetime(df[column])
            else:
                df[column] = df[column].astype(new_type)
            st.success(f"Changed data type of {column} to {new_type}")
        except:
            st.error(f"Could not change data type of {column} to {new_type}")

def show_summary_statistics(df):
    st.write("Summary Statistics:")
    st.write(df.describe())

def show_unique_values(df):
    column = st.selectbox("Select a column to see unique values:", df.columns)
    unique_values = df[column].nunique()
    st.write(f"Number of unique values in {column}: {unique_values}")
    if unique_values <= 20:  # Limit to avoid overwhelming display
        st.write("Unique values:")
        st.write(df[column].unique())
    else:
        st.write("Too many unique values to display. Here's a sample:")
        st.write(df[column].sample(20).unique())