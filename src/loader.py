import pandas as pd
import os


# Define paths
RAW_PATH = 'data/raw/online_retail_II.xlsx'
PROCESSED_PATH = 'data/processed/cleaned_transactions.csv'

def load_and_clean_data():
    """
    1. Loads the raw Excel file (both sheets).
    2. Cleans column names.
    3. Handles cancellations.
    4. Saves a fast-loading CSV to data/processed.
    """
    if os.path.exists(PROCESSED_PATH):
        print(f"Loading Data from {PROCESSED_PATH}")
        return pd.read_csv(PROCESSED_PATH, parse_dates=['invoice_date'])

    print("Loading Raw Data...")
    
    # There are two sheets in the raw data, we need to load both of them
    xls = pd.ExcelFile(RAW_PATH)
    sheet1 = pd.read_excel(xls, 'Year 2009-2010')
    sheet2 = pd.read_excel(xls, 'Year 2010-2011')
    
    df = pd.concat([sheet1, sheet2], ignore_index=True)
    print(f"Loaded {len(df)} transactions")
    
    # Cleaning 
    print("Cleaning Data...")
    
    # 1. Standardize column names
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # 2. Drop rows with missing Customer ID
    df = df.dropna(subset=['customer_id'])
    
    # 3. Convert Invoice Date to datetime
    df['invoice_date'] = pd.to_datetime(df['invoicedate'])
    
    # 4. Create 'total_amount' column
    df['total_amount'] = df['quantity'] * df['price']
    
    # 5. handle cancellations
    df['is_cancellation'] = df['invoice'].astype(str).str.startswith('C')
    
    # Filter out cancellations for the main view
    df_clean = df[~df['is_cancellation'] & (df['quantity']>0)]
    
    # Save
    print(f"Saving processed data to {PROCESSED_PATH}")
    df_clean.to_csv(PROCESSED_PATH, index=False)
    
    print("Done Processing")
    return df_clean


if __name__ == "__main__":
    df = load_and_clean_data()
    print(df.head())
    print(f"Total revenue in dataset (in Pounds): {df['total_amount'].sum():,.2f}")
    
    