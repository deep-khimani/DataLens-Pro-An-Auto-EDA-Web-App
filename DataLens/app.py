import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.markdown("""
<div style="text-align: center; padding: 20px;">
    <h1 style="
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4, #45B7D1, #96CEB4, #FFEAA7);
        background-size: 400% 400%;
        animation: gradient 3s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    ">
        🚀 DataLens Pro
    </h1>
    <h3 style="
        color: #2C3E50;
        font-weight: 300;
        margin-top: 10px;
        font-size: 1.2rem;
        letter-spacing: 2px;
    ">
        ✨ INTELLIGENT DATA EXPLORATION & VISUALIZATION SUITE ✨
    </h3>
    <p style="
        color: #7F8C8D;
        font-style: italic;
        margin-top: 5px;
        font-size: 0.9rem;
    ">
        Unleash the power of automated exploratory data analysis
    </p>
</div>

<style>
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
</style>
""", unsafe_allow_html=True)

df = None
all_columns = []

with st.sidebar:
    st.header("Upload Your Data")
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")

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

if uploaded_file and df is not None:
    st.header("Data Preview")
    
    if table_option == "Show Full Data":
        st.dataframe(df)
    elif table_option == "Show First 5 Rows":
        st.dataframe(df.head())
    elif table_option == "Show Last 5 Rows":
        st.dataframe(df.tail())
    else:
        st.dataframe(df.sample(n=5, random_state=1))
    
    st.write("---")
    st.header("Column Statistics")
    st.write(df.describe())
    
    st.write("---")
    st.header("Visualization")
    
    if x_axis_column == "None" and y_axis_column == "None":
        st.info("Please select columns for X and Y axes in the sidebar to generate a plot.")
    elif (plot_type in ["Histogram", "Box Plot", "Violin Plot"]) and x_axis_column == "None":
        st.info("Please select a column for the X-axis to generate this plot type.")
    elif x_axis_column != "None" or y_axis_column != "None":
        fig, ax = plt.subplots()
        
        if plot_type == "Scatter Plot":
            st.subheader(f"Scatter Plot: {x_axis_column} vs {y_axis_column}")
            if x_axis_column != "None" and y_axis_column != "None":
                sns.scatterplot(data=df, x=x_axis_column, y=y_axis_column, ax=ax)
            else:
                st.warning("Scatter plot requires both X and Y axes to be selected.")
        
        elif plot_type == "Line Plot":
            st.subheader(f"Line Plot: {x_axis_column} vs {y_axis_column}")
            if x_axis_column != "None" and y_axis_column != "None":
                sns.lineplot(data=df, x=x_axis_column, y=y_axis_column, ax=ax)
            else:
                st.warning("Line plot requires both X and Y axes to be selected.")
                
        elif plot_type == "Bar Plot":
            st.subheader(f"Bar Plot: {x_axis_column} vs {y_axis_column}")
            if x_axis_column != "None" and y_axis_column != "None":
                sns.barplot(data=df, x=x_axis_column, y=y_axis_column, ax=ax)
            else:
                st.warning("Bar plot requires both X and Y axes to be selected.")
        
        elif plot_type == "Histogram":
            st.subheader(f"Histogram of {x_axis_column}")
            if x_axis_column != "None":
                sns.histplot(data=df, x=x_axis_column, kde=True, ax=ax)
            else:
                st.warning("Please select a column for the X-axis to generate a histogram.")
                
        elif plot_type == "Box Plot":
            st.subheader(f"Box Plot of {x_axis_column}")
            if x_axis_column != "None":
                sns.boxplot(data=df, x=x_axis_column, ax=ax)
            else:
                st.warning("Please select a column for the X-axis to generate a box plot.")
        
        elif plot_type == "Violin Plot":
            st.subheader(f"Violin Plot of {x_axis_column}")
            if x_axis_column != "None":
                sns.violinplot(data=df, x=x_axis_column, ax=ax)
            else:
                st.warning("Please select a column for the X-axis to generate a violin plot.")

        st.pyplot(fig)
        plt.close(fig)