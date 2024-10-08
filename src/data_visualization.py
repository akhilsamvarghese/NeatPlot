import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

def visualize_data(df):
    

    if df is None or df.empty:
        st.warning("No data available for visualization. Please load and process data first.")
        return

    st.write("Select a visualization category:")
    viz_category = st.selectbox("Visualization Category", 
                                ["Univariate Analysis", 
                                 "Bivariate Analysis", 
                                 "3D Scatter Plot"])

    if viz_category == "Univariate Analysis":
        univariate_analysis(df)
    elif viz_category == "Bivariate Analysis":
        bivariate_analysis(df)
    elif viz_category == "3D Scatter Plot":
        show_3d_scatter_plot(df)

def univariate_analysis(df):
    st.subheader("Univariate Analysis")
    
    analysis_type = st.selectbox("Select Analysis Type", 
                                 ["Summary Statistics", "Histogram", "Box Plot", "Violin Plot", "Bar Chart"])
    
    if analysis_type == "Summary Statistics":
        show_summary_statistics(df)
    elif analysis_type == "Histogram":
        show_histogram(df)
    elif analysis_type == "Box Plot":
        show_box_plot(df)
    elif analysis_type == "Violin Plot":
        show_violin_plot(df)
    elif analysis_type == "Bar Chart":
        show_univariate_bar_chart(df)

def bivariate_analysis(df):
    st.subheader("Bivariate Analysis")
    
    analysis_type = st.selectbox("Select Analysis Type", 
                                 ["Scatter Plot", "Correlation Heatmap", "Group Box Plot", "Bar Chart"])
    
    if analysis_type == "Scatter Plot":
        show_scatter_plot(df)
    elif analysis_type == "Correlation Heatmap":
        show_correlation_heatmap(df)
    elif analysis_type == "Group Box Plot":
        show_group_box_plot(df)
    elif analysis_type == "Bar Chart":
        show_bivariate_bar_chart(df)

def show_summary_statistics(df):
    st.write("Summary Statistics")
    columns = st.multiselect("Select columns for summary statistics:", df.columns.tolist(), default=df.select_dtypes(include=[np.number]).columns.tolist())
    if columns:
        st.write(df[columns].describe())
    else:
        st.warning("Please select at least one column for summary statistics.")

def show_histogram(df):
    st.write("Histogram")
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    column = st.selectbox("Select a column", numeric_columns)
    bins = st.slider("Number of bins", min_value=5, max_value=100, value=30)
    fig = px.histogram(df, x=column, nbins=bins, title=f"Histogram of {column}")
    st.plotly_chart(fig)

def show_box_plot(df):
    st.write("Box Plot")
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    column = st.selectbox("Select a column", numeric_columns)
    fig = px.box(df, y=column, title=f"Box Plot of {column}")
    st.plotly_chart(fig)

def show_violin_plot(df):
    st.write("Violin Plot")
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    column = st.selectbox("Select a column", numeric_columns)
    fig = px.violin(df, y=column, box=True, points="all", title=f"Violin Plot of {column}")
    st.plotly_chart(fig)

def show_univariate_bar_chart(df):
    st.write("Univariate Bar Chart")
    columns = df.columns.tolist()
    column = st.selectbox("Select a column", columns)
    
    if df[column].dtype in ['int64', 'float64']:
        data = df[column].value_counts().sort_index()
    else:
        data = df[column].value_counts()
    
    fig = go.Figure(data=[go.Bar(
        x=data.index,
        y=data.values,
        marker_color='lightblue',
        marker_line_color='darkblue',
        marker_line_width=1.5,
        opacity=0.8
    )])
    
    fig.update_layout(
        title=f"Bar Chart of {column}",
        xaxis_title=column,
        yaxis_title="Count",
        bargap=0.2,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12)
    )
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='lightgray', gridcolor='lightgray')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='lightgray', gridcolor='lightgray')
    
    st.plotly_chart(fig)

def show_scatter_plot(df):
    st.write("Scatter Plot")
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    
    x_axis = st.selectbox("Select X-axis", numeric_columns, index=0)
    y_axis = st.selectbox("Select Y-axis", numeric_columns, index=min(1, len(numeric_columns)-1))
    
    color_palettes = ["Viridis", "Cividis", "Plasma", "Inferno", "Magma", "Turbo", "Jet", "Rainbow", "Portland", "Bluered", "Electric"]
    selected_palette = st.selectbox("Select color palette", color_palettes)
    
    fig = px.scatter(df, x=x_axis, y=y_axis, color=df[y_axis], 
                     color_continuous_scale=selected_palette, 
                     title=f"{y_axis} vs {x_axis} with Gradient on Y-axis")
    
    st.plotly_chart(fig)

def show_correlation_heatmap(df):
    st.write("Correlation Heatmap")
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    selected_columns = st.multiselect("Select columns for correlation heatmap:", numeric_columns, default=numeric_columns)
    
    if len(selected_columns) < 2:
        st.warning("Please select at least two numeric columns for the correlation heatmap.")
        return
    
    corr_matrix = df[selected_columns].corr()

    fig = px.imshow(corr_matrix, 
                    text_auto=True, 
                    aspect="auto", 
                    title="Correlation Heatmap",
                    width=900,
                    height=700)
    
    st.plotly_chart(fig)

def show_group_box_plot(df):
    st.write("Group Box Plot")
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    y_column = st.selectbox("Select Y-axis (numeric column)", numeric_columns)
    x_column = st.selectbox("Select X-axis (categorical column)", categorical_columns)
    
    fig = px.box(df, x=x_column, y=y_column, title=f"Box Plot of {y_column} grouped by {x_column}")
    st.plotly_chart(fig)

def show_bivariate_bar_chart(df):
    st.write("Bivariate Bar Chart")
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
    
    x_column = st.selectbox("Select X-axis (categorical column)", categorical_columns)
    y_column = st.selectbox("Select Y-axis (numeric column)", numeric_columns)
    
    data = df.groupby(x_column)[y_column].mean().sort_values(ascending=False)
    
    fig = go.Figure(data=[go.Bar(
        x=data.index,
        y=data.values,
        marker_color='lightgreen',
        marker_line_color='darkgreen',
        marker_line_width=1.5,
        opacity=0.8
    )])
    
    fig.update_layout(
        title=f"Bar Chart of {y_column} by {x_column}",
        xaxis_title=x_column,
        yaxis_title=f"Average {y_column}",
        bargap=0.2,
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(size=12)
    )
    
    fig.update_xaxes(showline=True, linewidth=2, linecolor='lightgray', gridcolor='lightgray')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='lightgray', gridcolor='lightgray')
    
    st.plotly_chart(fig)

def show_3d_scatter_plot(df):
    st.write("3D Scatter Plot")
    numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_columns) < 3:
        st.warning("Need at least three numeric columns for a 3D scatter plot.")
        return

    x_axis = st.selectbox("Select X-axis", numeric_columns, index=0)
    y_axis = st.selectbox("Select Y-axis", numeric_columns, index=1)
    z_axis = st.selectbox("Select Z-axis", numeric_columns, index=2)

    color_column = st.selectbox("Select Color Column (for gradient)", numeric_columns, index=3)
    
    color_palettes = ["Viridis", "Cividis", "Plasma", "Inferno", "Magma", "Turbo", "Jet", "Rainbow", "Portland", "Bluered", "Electric"]
    selected_palette = st.selectbox("Select color palette", color_palettes)

    fig = px.scatter_3d(df, x=x_axis, y=y_axis, z=z_axis, color=color_column,
                        color_continuous_scale=selected_palette,
                        title=f"3D Scatter Plot: {x_axis}, {y_axis}, {z_axis} (Color by {color_column})")

    st.plotly_chart(fig)