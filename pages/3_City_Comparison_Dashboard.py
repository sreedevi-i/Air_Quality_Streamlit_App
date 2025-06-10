import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_clean_data

st.set_page_config(page_title="Comparison Dashboard", layout="wide")

# Ensuring df_clean is initialized
if 'df_clean' not in st.session_state:
    load_clean_data()

df_clean = st.session_state.df_clean

st.title("City Comparison Dashboard")

# Date filter option
use_date_filter = st.checkbox("Compare by Date Range")

# Chart type selection outside form
chart_type = st.selectbox("Select Chart Type", ["Bar Chart", "Boxplot", "Summary Table"])

# Comparison form
with st.form(key='city_comparison_form'):
    st.subheader("Select Comparison Options")

    # City selection
    city_options = sorted(df_clean['City'].unique().tolist())
    selected_cities = st.multiselect("Select Cities to Compare", city_options, default=city_options[0])

    # Date range filter
    if use_date_filter:
        min_date = df_clean['Date'].min().date()
        max_date = df_clean['Date'].max().date()
        date_range = st.date_input("Select Date Range", value=[min_date, max_date], min_value=min_date, max_value=max_date)

    # Metric selection
    selected_metric = st.selectbox("Select Metric to Compare", ['AQI', 'PM2.5', 'PM10', 'CO', 'NO2', 'SO2', 'O3'])

    compare_button = st.form_submit_button(label='Compare')

# Comparison logic
if compare_button:
    # Apply filters
    filtered_df = df_clean.copy()

    # Filter by city
    filtered_df = filtered_df[filtered_df['City'].isin(selected_cities)]

    # Filter by date if enabled
    if use_date_filter:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered_df = filtered_df[(filtered_df['Date'] >= start_date) & (filtered_df['Date'] <= end_date)]

    # Checking if at least two cities are selected
    if len(selected_cities) < 2:
        st.warning("Please select at least two cities to compare.")
    else:
        # Showing comparison message
        st.write(f"**Comparison of Cities:** {', '.join(selected_cities)} on metric {selected_metric} by chart type {chart_type}")


        # Displaying result
        st.subheader("Comparison Result")

        if chart_type == "Bar Chart":
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

            # Preparing chart data for export
            chart_data = avg_metric_df.copy()

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
                legend_title="City"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Preparing chart data for export
            chart_data = filtered_df[['City', 'Date', selected_metric]].copy()

        elif chart_type == "Summary Table":
            summary_df = filtered_df.groupby('City')[selected_metric].agg(['count', 'mean', 'std', 'min', 'max']).reset_index()
            st.dataframe(summary_df)

            # Preparing chart data for export
            chart_data = summary_df.copy()

        # Exporting comparison data
        st.subheader("Export Comparison Data")
        chart_data_csv = chart_data.to_csv(index=False).encode('utf-8')

        filename_parts = ["city_comparison"]

        cities_str_for_filename = "_".join([city.replace(" ", "_") for city in selected_cities])
        filename_parts.append(cities_str_for_filename)

        if use_date_filter:
            filename_parts.append(f"{start_date.date()}_to_{end_date.date()}")

        filename_parts.append(chart_type.replace(" ", "_"))
        filename_parts.append(selected_metric)

        final_chart_filename = "_".join(filename_parts) + ".csv"

        st.download_button(
            label="Export Comparison Data to CSV",
            data=chart_data_csv,
            file_name=final_chart_filename,
            mime="text/csv"
        )
