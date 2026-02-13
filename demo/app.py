# demo/app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sales Seasonality Dashboard", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    # Load the processed CSV
    df = pd.read_csv('data/processed/cleaned_transactions.csv')
    df['invoice_date'] = pd.to_datetime(df['invoice_date'])
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ Data not found! Please run 'src/loader.py' first.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")
years = df['invoice_date'].dt.year.unique()
selected_years = st.sidebar.multiselect("Select Years", years, default=years)

# Filter data
df_filtered = df[df['invoice_date'].dt.year.isin(selected_years)]

# --- MAIN ANALYSIS: REVENUE OVER TIME ---
st.title("📈 Retail Seasonality Analysis")
st.markdown("Identify peak sales months to optimize inventory planning.")

# Top KPIs
monthly_sales = df_filtered.set_index('invoice_date').resample('M')['total_amount'].sum().reset_index()
total_rev = df_filtered['total_amount'].sum()
best_month_row = monthly_sales.loc[monthly_sales['total_amount'].idxmax()]

col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"£{total_rev:,.0f}")
col2.metric("Best Month", best_month_row['invoice_date'].strftime('%B %Y'), f"£{best_month_row['total_amount']:,.0f}")
col3.metric("Total Transactions", f"{len(df_filtered):,}")

# Chart 1: Monthly Trend
st.subheader("Monthly Revenue Trajectory")
fig_monthly = px.line(
    monthly_sales, 
    x='invoice_date', 
    y='total_amount',
    markers=True,
    labels={'total_amount': 'Revenue (£)', 'invoice_date': 'Date'}
)
fig_monthly.update_layout(xaxis_dtick="M1")
st.plotly_chart(fig_monthly, use_container_width=True)

# --- DEEP DIVE: DAY & HOUR ---
st.markdown("---")
st.subheader("🗓️ When do customers buy?")

# Prepare Data
df_filtered['day_of_week'] = df_filtered['invoice_date'].dt.day_name()
df_filtered['hour'] = df_filtered['invoice_date'].dt.hour

# Sort Days Correctly
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sunday']
daily_sales = df_filtered.groupby('day_of_week')['total_amount'].sum().reindex(days_order).reset_index()
hourly_sales = df_filtered.groupby('hour')['total_amount'].sum().reset_index()

# Create Two Columns for Charts
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.markdown("**Best Day of Week**")
    fig_day = px.bar(daily_sales, x='day_of_week', y='total_amount', color_discrete_sequence=['#1f77b4'])
    st.plotly_chart(fig_day, use_container_width=True)

with row2_col2:
    st.markdown("**Best Hour of Day**")
    fig_hour = px.bar(hourly_sales, x='hour', y='total_amount', color_discrete_sequence=['#ff7f0e'])
    st.plotly_chart(fig_hour, use_container_width=True)

# --- INSIGHTS SECTION ---
st.info("""
**💡 Operational Insights:**
1.  **Staffing:** Thursday is the busiest day. Ensure customer support is fully staffed.
2.  **Marketing:** The 'Lunch Rush' (12 PM) is real. Schedule email campaigns for 11:30 AM.
3.  **Inventory:** November is critical. Stock levels must be increased by 40% starting in October.
""")