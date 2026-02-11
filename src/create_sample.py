import pandas as pd
import os

# Define paths
RAW_PATH = 'data/raw/online_retail_II.xlsx'
SAMPLE_PATH = 'data/sample/sample_data.csv'

def create_sample():
    print("Loading Raw Data...")
    # Loading only first 1000 rows for sampling
    df = pd.read_excel(RAW_PATH, nrows=1000)
    
    # save as csv 
    df.to_csv(SAMPLE_PATH, index=False)
    print(f"Sample data saved to {SAMPLE_PATH}")
    
if __name__ == "__main__":
    if os.path.exists(RAW_PATH):
        create_sample()
    else:
        print(f"Raw data file not found at {RAW_PATH}, please the data from the source and save it to the data/raw folder.")