# eda_functions.py
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def show_data_preview(df, table_option):
    st.header("Data Preview")
    if table_option == "Show Full Data":
        st.dataframe(df)
    elif table_option == "Show First 5 Rows":
        st.dataframe(df.head())
    elif table_option == "Show Last 5 Rows":
        st.dataframe(df.tail())
    else:
        st.dataframe(df.sample(n=5, random_state=1))


def show_statistics(df):
    st.write("---")
    st.header("Column Statistics")
    st.write(df.describe())


def plot_data(df, x_axis_column, y_axis_column, plot_type):
    st.write("---")
    st.header("Visualization")
    
    if x_axis_column == "None" and y_axis_column == "None":
        st.info("Please select columns for X and Y axes in the sidebar to generate a plot.")
        return
    
    if plot_type in ["Histogram", "Box Plot", "Violin Plot"] and x_axis_column == "None":
        st.info("Please select a column for the X-axis to generate this plot type.")
        return
    
    if x_axis_column == "None" and y_axis_column != "None":
        st.warning("X-axis column must be selected if Y-axis is selected.")
        return
    
    fig, ax = plt.subplots()
    
    if plot_type == "Scatter Plot":
        if x_axis_column != "None" and y_axis_column != "None":
            sns.scatterplot(data=df, x=x_axis_column, y=y_axis_column, ax=ax)
            st.subheader(f"Scatter Plot: {x_axis_column} vs {y_axis_column}")
        else:
            st.warning("Scatter plot requires both X and Y axes to be selected.")
    
    elif plot_type == "Line Plot":
        if x_axis_column != "None" and y_axis_column != "None":
            sns.lineplot(data=df, x=x_axis_column, y=y_axis_column, ax=ax)
            st.subheader(f"Line Plot: {x_axis_column} vs {y_axis_column}")
        else:
            st.warning("Line plot requires both X and Y axes to be selected.")
    
    elif plot_type == "Bar Plot":
        if x_axis_column != "None" and y_axis_column != "None":
            sns.barplot(data=df, x=x_axis_column, y=y_axis_column, ax=ax)
            st.subheader(f"Bar Plot: {x_axis_column} vs {y_axis_column}")
        else:
            st.warning("Bar plot requires both X and Y axes to be selected.")
    
    elif plot_type == "Histogram":
        sns.histplot(data=df, x=x_axis_column, kde=True, ax=ax)
        st.subheader(f"Histogram of {x_axis_column}")
    
    elif plot_type == "Box Plot":
        sns.boxplot(data=df, x=x_axis_column, ax=ax)
        st.subheader(f"Box Plot of {x_axis_column}")
    
    elif plot_type == "Violin Plot":
        sns.violinplot(data=df, x=x_axis_column, ax=ax)
        st.subheader(f"Violin Plot of {x_axis_column}")
    
    st.pyplot(fig)
    plt.close(fig)
