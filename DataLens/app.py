import streamlit as st
from style import show_header
from data_loader import upload_data
from ui_components import sidebar_controls
from eda_functions import show_data_preview, show_statistics, plot_data

def main():
    show_header()
    df = upload_data()
    
    if df is not None:
        table_option, x_axis_column, y_axis_column, plot_type = sidebar_controls(df)
        
        show_data_preview(df, table_option)
        show_statistics(df)
        plot_data(df, x_axis_column, y_axis_column, plot_type)

if __name__ == "__main__":
    main()
