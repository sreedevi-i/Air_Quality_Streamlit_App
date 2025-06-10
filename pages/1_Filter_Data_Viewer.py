import streamlit as st
import pandas as pd
import pandasql as ps
from utils import load_clean_data

st.set_page_config(page_title="Filters Data Viewer", layout="wide")

st.title("Filters Data Viewer")

# Loading cleaned df from session_state
if 'df_clean' not in st.session_state:
    load_clean_data()
df_clean = st.session_state.df_clean

### Filter options
st.subheader("Filter Options")
use_city_filter = st.checkbox("Filter by City")
use_date_filter = st.checkbox("Filter by Date Range")
use_aqi_filter = st.checkbox("Filter by AQI Range")
use_pm25_filter = st.checkbox("Filter by PM2.5 Range")
use_co_filter = st.checkbox("Filter by CO Range")
use_no2_filter = st.checkbox("Filter by NO2 Range")
use_so2_filter = st.checkbox("Filter by SO2 Range")
use_o3_filter = st.checkbox("Filter by O3 Range")
use_pm10_filter = st.checkbox("Filter by PM10 Range")

### Now the actual form → will run only on Search click
with st.form(key='data_filter_form'):
    st.subheader("Select Filters")

    # City
    if use_city_filter:
        city_options = sorted(df_clean['City'].unique().tolist())
        selected_cities = st.multiselect("Select Cities", city_options, default=city_options[0])

    # Date range
    if use_date_filter:
        min_date = df_clean['Date'].min().date()
        max_date = df_clean['Date'].max().date()
        date_range = st.date_input("Select Date Range", value=[min_date, max_date], min_value=min_date, max_value=max_date)

    # AQI
    if use_aqi_filter:
        aqi_min = st.number_input("Min AQI", value=float(df_clean['AQI'].min()), step=1.0)
        aqi_max = st.number_input("Max AQI", value=float(df_clean['AQI'].max()), step=1.0)

    # PM2.5
    if use_pm25_filter:
        pm25_min = st.number_input("Min PM2.5", value=float(df_clean['PM2.5'].min()), step=0.1)
        pm25_max = st.number_input("Max PM2.5", value=float(df_clean['PM2.5'].max()), step=0.1)

    # CO
    if use_co_filter:
        co_min = st.number_input("Min CO", value=float(df_clean['CO'].min()), step=1.0)
        co_max = st.number_input("Max CO", value=float(df_clean['CO'].max()), step=1.0)

    # NO2
    if use_no2_filter:
        no2_min = st.number_input("Min NO2", value=float(df_clean['NO2'].min()), step=0.1)
        no2_max = st.number_input("Max NO2", value=float(df_clean['NO2'].max()), step=0.1)

    # SO2
    if use_so2_filter:
        so2_min = st.number_input("Min SO2", value=float(df_clean['SO2'].min()), step=0.1)
        so2_max = st.number_input("Max SO2", value=float(df_clean['SO2'].max()), step=0.1)

    # O3
    if use_o3_filter:
        o3_min = st.number_input("Min O3", value=float(df_clean['O3'].min()), step=0.1)
        o3_max = st.number_input("Max O3", value=float(df_clean['O3'].max()), step=0.1)

    # PM10
    if use_pm10_filter:
        pm10_min = st.number_input("Min PM10", value=float(df_clean['PM10'].min()), step=0.1)
        pm10_max = st.number_input("Max PM10", value=float(df_clean['PM10'].max()), step=0.1)

    # Submit button
    submit_button = st.form_submit_button(label='Search')

### When user clicks Search
if submit_button:
    where_clauses = []

    # City
    if use_city_filter:
        cities_str = "', '".join(selected_cities)
        where_clauses.append(f"City IN ('{cities_str}')")

    # Date range
    if use_date_filter:
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        where_clauses.append(f"Date >= '{start_date}' AND Date <= '{end_date}'")

    # AQI
    if use_aqi_filter:
        where_clauses.append(f"AQI >= {aqi_min} AND AQI <= {aqi_max}")

    # PM2.5
    if use_pm25_filter:
        where_clauses.append(f"`PM2.5` >= {pm25_min} AND `PM2.5` <= {pm25_max}")

    # CO
    if use_co_filter:
        where_clauses.append(f"CO >= {co_min} AND CO <= {co_max}")

    # NO2
    if use_no2_filter:
        where_clauses.append(f"NO2 >= {no2_min} AND NO2 <= {no2_max}")

    # SO2
    if use_so2_filter:
        where_clauses.append(f"SO2 >= {so2_min} AND SO2 <= {so2_max}")

    # O3
    if use_o3_filter:
        where_clauses.append(f"O3 >= {o3_min} AND O3 <= {o3_max}")

    # PM10
    if use_pm10_filter:
        where_clauses.append(f"`PM10` >= {pm10_min} AND `PM10` <= {pm10_max}")

    # Build final SQL query
    where_clause_str = " AND ".join(where_clauses)
    if where_clause_str:
        sql_query = f"SELECT * FROM df_clean WHERE {where_clause_str}"
    else:
        sql_query = "SELECT * FROM df_clean"  # No filters applied

    # Run query
    filtered_df = ps.sqldf(sql_query, locals())

    # Show results
    st.subheader("Filtered Air Quality Data")
    st.write(f"**Filters applied:** {where_clause_str if where_clause_str else 'None'}")
    st.dataframe(filtered_df)

    # Build dynamic filename
    filename_parts = ["filtered_air_quality"]

    if use_city_filter:
        cities_str_for_filename = "_".join([city.replace(" ", "_") for city in selected_cities])
        filename_parts.append(cities_str_for_filename)

    if use_date_filter:
        filename_parts.append(f"{start_date.date()}_to_{end_date.date()}")

    final_filename = "_".join(filename_parts) + ".csv"

    # Export CSV button
    csv_data = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Export Filtered Data to CSV",
        data=csv_data,
        file_name=final_filename,
        mime="text/csv"
    )

    st.success(f"Found {len(filtered_df)} records.")
