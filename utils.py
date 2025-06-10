import pandas as pd
import streamlit as st
import plotly.express as px
import io

def load_css(file_name):
    with open(file_name) as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def load_raw_data():
    """Loading the raw data and stores it in st.session_state.df_raw"""
    if 'df_raw' not in st.session_state:
        df = pd.read_csv("Air_Quality.csv")
        st.session_state.df_raw = df

def show_df_info(df):
    """Displaying df.info() output as text"""
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()

    with st.expander("Click to view df.info() output"):
        st.code(info_str, language='text')

def perform_missing_value_analysis(df):
    """Displaying missing value analysis table"""
    st.write("#### Missing Values Analysis")
    missing_values = df.isnull().sum()
    missing_percent = (missing_values / len(df)) * 100

    missing_df = pd.DataFrame({
        'Column': missing_values.index,
        'Missing Count': missing_values.values,
        'Missing %': missing_percent.values
    })

    st.dataframe(missing_df)

    co2_missing_percent = missing_percent['CO2']
    st.write(f"CO2 column has {co2_missing_percent:.2f}% missing values. This column will be dropped.")

def perform_outlier_analysis(df):
    """Visualizing outliers with boxplots and applies outlier filtering"""
    st.write("#### Outlier Analysis")
    st.write("The outliers for each feature are visualized with boxplots below")

    numeric_columns = df.select_dtypes(include='number').columns

    with st.expander("Click to view boxplots for all numeric columns"):
        for col in numeric_columns:
            st.write(f"#### Boxplot for `{col}`")
            fig = px.box(df, y=col)
            st.plotly_chart(fig, use_container_width=True)

            # Calculating IQR bounds
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            # Calculating actual min/max in current data
            actual_min = df[col].min()
            actual_max = df[col].max()

            # Clipping the bounds for user message
            lower_bound_clipped = max(lower_bound, actual_min)
            upper_bound_clipped = min(upper_bound, actual_max)

            # Displaying message with clipped values
            st.write(f"**{col}:** Keeping values between {lower_bound_clipped:.2f} and {upper_bound_clipped:.2f}")

            # Applying actual filtering
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

    return df


def load_clean_data():
    """Loading, cleaning data, and storing result in st.session_state.df_clean"""
    # Ensuring raw data is loaded
    load_raw_data()
    df = st.session_state.df_raw.copy()

    st.write("#### Steps taken for data cleaning")
    st.write("""
    - The **'Date'** column is stored as a string. This should be converted to Date.
    - The **'CO2'** column has ~82% missing values. This should be dropped.
    - We can see the outliers detected in few features of dataset.
    """)

    # Converting to Date
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.tz_localize(None)

    # Dropping CO2 column
    df = df.drop(columns=['CO2'])

    # Performing outlier analysis and filtering
    df = perform_outlier_analysis(df)

    # Dropping remaining NaNs and reset index
    df_clean = df.dropna().reset_index(drop=True)

    # Storing in session_state
    st.session_state.df_clean = df_clean
