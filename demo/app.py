import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Sales Seasonality Dashboard", layout="wide")

# Data loading
@st.cache_data
def load_data():
    # Load the processed CSV
    df = pd.read_csv('data/processed/cleaned_transactions.csv')
    
    # ensure date is datetime
    df['invoice_date'] = pd.to_datetime(df['invoice_date'])
    return df

try:
    df=load_data()
except FileNotFoundError:
    st.error("Data not found")
    st.stop()