# demo/app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- PAGE CONFIG ---
st.set_page_config(page_title="Sales Seasonality & Segments", layout="wide")

# --- DATA LOADING ---
@st.cache_data
def load_data():
    df = pd.read_csv('data/processed/cleaned_transactions.csv')
    df['invoice_date'] = pd.to_datetime(df['invoice_date'])
    return df

@st.cache_data
def calculate_rfm(df):
    # Snapshot date = last date + 1 day
    snapshot_date = df['invoice_date'].max() + pd.Timedelta(days=1)
    
    # Calculate R, F, M
    rfm = df.groupby('customer_id').agg({
        'invoice_date': lambda x: (snapshot_date - x.max()).days,
        'invoice': 'nunique',
        'total_amount': 'sum'
    }).reset_index()
    
    rfm.rename(columns={'invoice_date': 'recency', 'invoice': 'frequency', 'total_amount': 'monetary'}, inplace=True)
    
    # Calculate Scores (1-5)
    rfm['r_score'] = pd.qcut(rfm['recency'], 5, labels=[5, 4, 3, 2, 1])
    rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])
    rfm['m_score'] = pd.qcut(rfm['monetary'], 5, labels=[1, 2, 3, 4, 5])
    
    # Segment Logic
    rfm['rf_score'] = rfm['r_score'].astype(str) + rfm['f_score'].astype(str)
    
    seg_map = {
        r'[1-2][1-2]': 'Hibernating',
        r'[1-2][3-4]': 'At Risk',
        r'[1-2]5': 'Can\'t Lose',
        r'3[1-2]': 'About To Sleep',
        r'33': 'Need Attention',
        r'[3-4][4-5]': 'Loyal Customers',
        r'41': 'Promising',
        r'51': 'New Customers',
        r'[4-5][2-3]': 'Potential Loyalists',
        r'5[4-5]': 'Champions'
    }
    rfm['segment'] = rfm['rf_score'].replace(seg_map, regex=True)
    return rfm

try:
    df = load_data()
    rfm = calculate_rfm(df)
except FileNotFoundError:
    st.error("❌ Data not found! Please run 'src/loader.py' first.")
    st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")
years = df['invoice_date'].dt.year.unique()
selected_years = st.sidebar.multiselect("Select Years", years, default=years)
df_filtered = df[df['invoice_date'].dt.year.isin(selected_years)]

# --- MAIN LAYOUT ---
st.title("🛍️ Retail Intelligence Dashboard")

# Create Tabs
tab1, tab2 = st.tabs(["📈 Seasonality Analysis", "👥 Customer Segmentation"])

# --- TAB 1: SEASONALITY (Your Week 1 Work) ---
with tab1:
    st.subheader("Revenue Trends & Best Times")
    
    # Metrics
    total_rev = df_filtered['total_amount'].sum()
    monthly_sales = df_filtered.set_index('invoice_date').resample('M')['total_amount'].sum().reset_index()
    best_month = monthly_sales.loc[monthly_sales['total_amount'].idxmax()]
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"£{total_rev:,.0f}")
    c2.metric("Best Month", best_month['invoice_date'].strftime('%B %Y'))
    c3.metric("Total Txns", f"{len(df_filtered):,}")
    
    # Line Chart
    fig_line = px.line(monthly_sales, x='invoice_date', y='total_amount', markers=True, title="Monthly Revenue")
    st.plotly_chart(fig_line, use_container_width=True)
    
    # Day/Hour Analysis
    df_filtered['day'] = df_filtered['invoice_date'].dt.day_name()
    df_filtered['hour'] = df_filtered['invoice_date'].dt.hour
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Sunday']
    daily_sales = df_filtered.groupby('day')['total_amount'].sum().reindex(days_order).reset_index()
    hourly_sales = df_filtered.groupby('hour')['total_amount'].sum().reset_index()
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(px.bar(daily_sales, x='day', y='total_amount', title="Sales by Day"), use_container_width=True)
    with col_b:
        st.plotly_chart(px.bar(hourly_sales, x='hour', y='total_amount', title="Sales by Hour"), use_container_width=True)

# --- TAB 2: CUSTOMER SEGMENTS (New Week 2 Work) ---
with tab2:
    st.subheader("RFM Segmentation (Recency, Frequency, Monetary)")
    
    # Segment Count Bar Chart
    seg_counts = rfm['segment'].value_counts().reset_index()
    seg_counts.columns = ['Segment', 'Count']
    
    fig_bar = px.bar(seg_counts, x='Segment', y='Count', color='Segment', 
                     title="Distribution of Customer Segments",
                     color_discrete_sequence=px.colors.qualitative.Prism)
    st.plotly_chart(fig_bar, use_container_width=True)
    

    st.markdown("**Segment Value Analysis** (Size = Revenue Contribution)")
    fig_tree = px.treemap(rfm, path=['segment'], values='monetary', 
                          color='segment', title="Which segments drive the most revenue?")
    st.plotly_chart(fig_tree, use_container_width=True)
    
    # Drill Down
    st.markdown("---")
    st.markdown("### 🕵️ Customer Drill-Down")
    target_seg = st.selectbox("Select Segment to View:", rfm['segment'].unique())
    
    filtered_customers = rfm[rfm['segment'] == target_seg].sort_values(by='monetary', ascending=False)
    st.dataframe(filtered_customers.head(10), use_container_width=True)
    st.caption(f"Showing top 10 customers in '{target_seg}'")