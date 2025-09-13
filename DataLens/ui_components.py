# ui_components.py
import streamlit as st

def sidebar_controls(df):
    table_option = None
    x_axis_column = "None"
    y_axis_column = "None"
    plot_type = None
    all_columns = []

    if df is not None:
        st.header("Upload Your Data")
        
        st.write("---")
        st.subheader("Table Display")
        table_option = st.selectbox(
            "Select how you want to preview the data:",
            ("Show Full Data", "Show First 5 Rows", "Show Last 5 Rows", "Show Random Sample")
        )
        
        st.write("---")
        st.subheader("Visualization Settings")
        
        all_columns = df.columns.tolist()
        
        x_axis_column = st.selectbox(
            "Select column for X-axis:",
            options=["None"] + all_columns,
            index=0
        )
        
        y_axis_column = st.selectbox(
            "Select column for Y-axis:",
            options=["None"] + all_columns,
            index=0
        )
        
        plot_type = st.selectbox(
            "Select plot type:",
            ("Scatter Plot", "Line Plot", "Bar Plot", "Histogram", "Box Plot", "Violin Plot")
        )
    
    return table_option, x_axis_column, y_axis_column, plot_type
