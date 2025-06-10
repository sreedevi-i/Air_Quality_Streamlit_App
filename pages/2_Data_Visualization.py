import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_clean_data

st.set_page_config(page_title="Data Visualization", layout="wide")

# Ensuring df_clean is initialized
if 'df_clean' not in st.session_state:
    load_clean_data()

df_clean = st.session_state.df_clean

st.title("Data Visualization")

# Visualization options
st.subheader("Select Visualization Options")
use_city_filter = st.checkbox("By City")
use_date_filter = st.checkbox("By Date Range")

# Chart type selection
chart_type = st.selectbox("Select Chart Type", ["Line Chart", "Bar Chart", "Boxplot", "Scatter Plot"])

# Visualization form
with st.form(key='visualization_form'):
    st.subheader("Select Visualization Metric")

    # Metric selection based on chart type
    if chart_type in ["Line Chart", "Bar Chart", "Boxplot"]:
        selected_metric = st.selectbox("Select Metric", ['AQI', 'PM2.5', 'PM10', 'CO', 'NO2', 'SO2', 'O3'])
    elif chart_type == "Scatter Plot":
        selected_metric_x = st.selectbox("Select X-axis Metric", ['AQI', 'PM2.5', 'PM10', 'CO', 'NO2', 'SO2', 'O3'])
        selected_metric_y = st.selectbox("Select Y-axis Metric", ['AQI', 'PM2.5', 'PM10', 'CO', 'NO2', 'SO2', 'O3'])

    # City filter
    if use_city_filter:
        city_options = sorted(df_clean['City'].unique().tolist())
        selected_cities = st.multiselect("Select Cities", city_options, default=city_options[0])

    # Date range filter
    if use_date_filter:
        min_date = df_clean['Date'].min().date()
        max_date = df_clean['Date'].max().date()
        date_range = st.date_input("Select Date Range", value=[min_date, max_date], min_value=min_date, max_value=max_date)

    visualize_button = st.form_submit_button(label='Visualize')

# Visualization logic
if visualize_button:
    # Applying filters
    filtered_df = df_clean.copy()

    if use_city_filter:
        filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]

    if use_date_filter:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]

    # Showing resulting visualization chart
    st.subheader("Visualization Result")

    if chart_type == "Line Chart":
        fig = px.line(
            filtered_df,
            x='Date',
            y=selected_metric,
            color='City' if use_city_filter else None,
            title=f"{selected_metric} Trend Over Time"
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title=selected_metric,
            legend_title="City" if use_city_filter else None
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Bar Chart":
        avg_metric_df = filtered_df.groupby('City')[selected_metric].mean().reset_index().sort_values(by=selected_metric, ascending=False)
        fig = px.bar(
            avg_metric_df,
            x='City',
            y=selected_metric,
            text_auto=True,
            title=f"Average {selected_metric} by City"
        )
        fig.update_layout(
            xaxis_title="City",
            yaxis_title=f"Average {selected_metric}",
            legend_title=None
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Boxplot":
        fig = px.box(
            filtered_df,
            x='City',
            y=selected_metric,
            points="all",
            title=f"{selected_metric} Distribution by City"
        )
        fig.update_layout(
            xaxis_title="City",
            yaxis_title=selected_metric,
            legend_title="City" if use_city_filter else None
        )
        st.plotly_chart(fig, use_container_width=True)

    elif chart_type == "Scatter Plot":
        fig = px.scatter(
            filtered_df,
            x=selected_metric_x,
            y=selected_metric_y,
            color='City' if use_city_filter else None,
            title=f"{selected_metric_y} vs {selected_metric_x}"
        )
        fig.update_layout(
            xaxis_title=selected_metric_x,
            yaxis_title=selected_metric_y,
            legend_title="City" if use_city_filter else None
        )
        st.plotly_chart(fig, use_container_width=True)

    # Exporting chart data
    st.subheader("Export Chart Data")
    chart_data_csv = filtered_df.to_csv(index=False).encode('utf-8')

    filename_parts = ["chart_data"]

    if use_city_filter:
        cities_str_for_filename = "_".join([city.replace(" ", "_") for city in selected_cities])
        filename_parts.append(cities_str_for_filename)

    if use_date_filter:
        filename_parts.append(f"{start_date.date()}_to_{end_date.date()}")

    filename_parts.append(chart_type.replace(" ", "_"))

    final_chart_filename = "_".join(filename_parts) + ".csv"

    st.download_button(
        label="Export Chart Data to CSV",
        data=chart_data_csv,
        file_name=final_chart_filename,
        mime="text/csv"
    )
