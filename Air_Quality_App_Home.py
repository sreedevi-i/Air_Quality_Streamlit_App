import streamlit as st
from utils import load_raw_data, load_clean_data, show_df_info, perform_missing_value_analysis


st.set_page_config(page_title="Home", layout="wide")

st.title("Global Air Quality Dataset Explorer")

# Introduction / About the Data
st.markdown("""
## About the Dataset

This app uses the **Global Air Quality dataset**, which contains air quality measurements from multiple cities worldwide. The data includes daily measurements of key air quality indicators collected from various monitoring stations. The dataset provides an opportunity to analyze, visualize, and compare air pollution levels across different cities and over time.
""")

# Description of Data (Features)
st.markdown("""
## Dataset Features

- **Date**: Date of measurement  
- **City**: City where the measurement was recorded  
- **AQI**: Air Quality Index (aggregated index of overall air quality)  
- **PM2.5**: Fine particulate matter (diameter ≤ 2.5 microns)  
- **PM10**: Particulate matter (diameter ≤ 10 microns)  
- **CO**: Carbon Monoxide concentration  
- **NO2**: Nitrogen Dioxide concentration  
- **SO2**: Sulfur Dioxide concentration  
- **O3**: Ozone concentration  
- **CO2**: Carbon Dioxide concentration (**dropped during cleaning due to high missing values**)  
""")

# App Structure
st.markdown("""
## App Functionality and Navigation

This app consists of the following pages:

### 1. Air Quality App Home
- Provides an overview of the app functionality.
- Displays initial raw data and DataFrame info.
- Shows missing values analysis.
- Visualizes outliers with boxplots.
- Describes data cleaning.

### 2. Filtered Data Viewer (Explorer)
- Allows the user to filter the cleaned dataset interactively.
- Filters by City, Date Range, AQI, PM2.5, PM10, CO, NO2, SO2, O3.
- Provides an option to export the filtered data to CSV.

### 3. Data Visualization
- Enables flexible visualization of key metrics.
- Supports Line Chart, Bar Chart, Boxplot, Scatter Plot.
- Allows filtering by City and Date Range.
- Provides option to export chart data to CSV.

### 4. City Comparison Dashboard
- Designed to compare air quality metrics across multiple cities.
- Supports Bar Chart, Boxplot, and Summary Table views.
- Allows filtering by Date Range.
- Provides option to export comparison data to CSV.

---

Use the sidebar to navigate between pages and explore the dataset interactively.
""")

# Loading raw data
load_raw_data()
df = st.session_state.df_raw

# Displaying raw data
st.subheader("Raw Data (First 5 rows)")
st.dataframe(df.head())

# Displaying df.info()
st.subheader("DataFrame Info Summary")
show_df_info(df)

# Missing value analysis
perform_missing_value_analysis(df)

# Loading clean data (also performs outlier analysis)
load_clean_data()
df_clean = st.session_state.df_clean

# Displaying cleaned data
st.subheader("Cleaned Data (First 5 rows)")
st.dataframe(df_clean.head())

st.success(f"Final cleaned dataset shape: {df_clean.shape}")
