import os
import pandas as pd
from datetime import datetime
from .fetch_data import fetch_stock_data
from .storage import load_data_from_csv, save_data_to_csv

def update_csv_files(tickers):
    for ticker in tickers:
        try:
            # Fetch new data
            new_data = fetch_stock_data(ticker)
            new_df = pd.DataFrame(new_data)
            
            # Load existing data from CSV
            existing_data = load_data_from_csv(ticker)
            if existing_data is not None:
                existing_df = pd.DataFrame(existing_data)
                combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset='Date', keep='last')
            else:
                combined_df = new_df
            
            # Save the combined data back to CSV
            save_data_to_csv(combined_df.to_dict(orient='records'), ticker)
            print(f'Updated data for {ticker} successfully.')
        except Exception as e:
            print(f'Error updating data for {ticker}: {str(e)}')
