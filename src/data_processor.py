import streamlit as st
import pandas as pd
import numpy as np
import re

def process_data(df):
    
    st.write(df.head(11))
    # Step 1: Data Overview
    st.subheader("1. Data Overview")
    # st.write(df.head())
    st.write("Original Data Shape:", df.shape)
    st.write("Data Types:")
    st.dataframe(df.dtypes,use_container_width=True, width=100)
    st.write("Data Preview:")

    # Step 2: Select Columns
    st.subheader("2. Select Columns")
    selected_columns = st.multiselect("Select columns to keep:", df.columns.tolist(), default=df.columns.tolist())
    df = df[selected_columns]
    st.write("Selected Data Preview:")
    st.write(df.head())
    st.write("Selected Data Shape:", df.shape)

    # Step 3: Handle Missing Values
    st.subheader("3. Handle Missing Values")
    df = handle_missing_values(df)

    # Step 4: Convert Data Types
    st.subheader("4. Convert Data Types")
    df = convert_data_types(df)

    # Step 5: Remove Special Characters
    st.subheader("5. Remove Special Characters")
    df = remove_special_characters(df)

    # Final Step: Display Processed Data
    st.subheader("Final Processed Data")
    st.write(df.head())
    st.write("Final Data Shape:", df.shape)

    return df

def handle_missing_values(df):
    st.write("Columns with missing values:")
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    st.write(missing_cols)

    if not missing_cols.empty:
        columns_to_drop = st.multiselect("Select columns to drop (if any):", missing_cols.index.tolist())
        
        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)
            st.write(f"Dropped columns: {', '.join(columns_to_drop)}")

        remaining_missing = df.isnull().sum()
        remaining_missing_cols = remaining_missing[remaining_missing > 0]

        if not remaining_missing_cols.empty:
            st.write("Remaining columns with missing values:")
            st.write(remaining_missing_cols)

            method = st.radio("Choose method to handle remaining missing values:", 
                              ["Drop rows", "Fill with mean/mode", "Fill with median"])

            if method == "Drop rows":
                df = df.dropna()
                st.write("Rows with missing values have been dropped.")
            elif method == "Fill with mean/mode":
                for col in remaining_missing_cols.index:
                    if df[col].dtype in ['int64', 'float64']:
                        df[col].fillna(df[col].mean(), inplace=True)
                    else:
                        df[col].fillna(df[col].mode()[0], inplace=True)
                st.write("Missing values have been filled with mean/mode.")
            elif method == "Fill with median":
                for col in remaining_missing_cols.index:
                    if df[col].dtype in ['int64', 'float64']:
                        df[col].fillna(df[col].median(), inplace=True)
                    else:
                        df[col].fillna(df[col].mode()[0], inplace=True)
                st.write("Missing values have been filled with median.")

    st.write("Missing values after handling:")
    st.dataframe(df.isnull().sum(), use_container_width=True, height=500, width=100)
    return df

def convert_data_types(df):
    st.write("Current data types:")
    st.dataframe(df.dtypes, use_container_width=True, height=500, width=100)

    columns_to_convert = st.multiselect("Select columns to convert:", df.columns.tolist())

    for column in columns_to_convert:
        new_type = st.selectbox(f"Select new data type for {column}:", ["int", "float", "string", "datetime"], key=f"dtype_{column}")

        try:
            if new_type == "int":
                df[column] = df[column].astype(int)
            elif new_type == "float":
                df[column] = df[column].astype(float)
            elif new_type == "string":
                df[column] = df[column].astype(str)
            elif new_type == "datetime":
                df[column] = pd.to_datetime(df[column])
            st.success(f"Successfully converted {column} to {new_type}")
        except Exception as e:
            st.error(f"Error converting data type for {column}: {str(e)}")

    st.write("Updated data types:")
    st.dataframe(df.dtypes, use_container_width=True, height=500, width=100)
    return df



def remove_special_characters(df):
    st.write("Select columns to remove special characters:")
    string_columns = df.select_dtypes(include=['object']).columns
    columns_to_clean = st.multiselect("Choose columns:", string_columns)

    if columns_to_clean:
        special_chars = st.text_input("Enter special characters to remove (leave empty to remove all non-alphanumeric):", 
                                      value="!@#$%^&*()_+-={}[]|\\:;\"'<>,?/~`")
        
        if special_chars:
            pattern = f'[{re.escape(special_chars)}]'
        else:
            pattern = '[^a-zA-Z0-9\s]'
        
        for column in columns_to_clean:
            df[column] = df[column].astype(str).apply(lambda x: re.sub(pattern, '', x))
            st.write(f"Removed special characters from {column}")
        
        st.write("Preview after removing special characters:")
        st.write(df[columns_to_clean].head())
    else:
        st.write("No columns selected for special character removal.")

    return df


