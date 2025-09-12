# DataLens Pro: An Auto EDA Web App

**DataLens** is a powerful and intuitive Streamlit application that allows you to perform automatic Exploratory Data Analysis (EDA) on your CSV files with just a few clicks. Upload your data, and the app will generate a data preview, key statistics, and interactive visualizations, helping you quickly gain insights into your dataset.

## ✨ Features

  * **Easy File Upload**: Simply drag and drop your CSV file to get started.
  * **Flexible Data Preview**: View the full dataset, or a sample of the first, last, or random rows.
  * **Automated Statistics**: Get a comprehensive summary of your data, including count, mean, standard deviation, and more.
  * **Interactive Visualizations**: Select columns for the X and Y axes and choose from a variety of plot types to visualize relationships and distributions.
      * **Plot Options**:
          * Scatter Plot
          * Line Plot
          * Bar Plot
          * Histogram
          * Box Plot
          * Violin Plot

## 🌐 Live Application

You can access the deployed version of the app here:

**[https://datalens-auto-eda.streamlit.app/](https://datalens-auto-eda.streamlit.app/)**

-----

## 💻 How to Run the App Locally

### Prerequisites

Make sure you have Python installed on your system.

### Installation

1.  Clone this repository to your local machine:
    ```bash
    git clone https://github.com/deep-khimani/DataLens-Pro-An-Auto-EDA-Web-App.git
    cd DataLens-Pro-An-Auto-EDA-Web-App
    ```
2.  Install the required Python libraries using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

### Running the App

1.  Navigate into the `DataLens` folder where the `app.py` file is located:
    ```bash
    cd DataLens
    ```
2.  Run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
3.  The app will automatically open in your web browser. If it doesn't, navigate to `http://localhost:8501`.

-----

## 📂 Project Structure

```
├── DataLens/         
│   ├── app.py        
├── requirements.txt  
└── README.md         
```

-----

## 🤝 Contributing

Contributions are welcome\! If you have suggestions for new features, bug fixes, or improvements, feel free to open an issue or submit a pull request.
