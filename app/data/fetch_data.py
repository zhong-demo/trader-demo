import yfinance as yf
import logging
import os
import pandas as pd
from .storage import save_data_to_csv
from .process_data import clean_data

DATA_DIR = './app/data/tickers/'  # Directory to store CSV files


def fetch_stock_data(ticker, start=None, end=None):
    
    # Try to load data from CSV
    data = fetch_from_storage(ticker, start, end)
    
    if data is not None:
        logging.info(f'Data loaded from CSV for ticker: {ticker}')
        return data
    
    logging.info(f'Fetching data from Yahoo Finance for ticker: {ticker}')

    # if start and end date are not provided, set them to the default values
    if start is None:
        start = '2000-01-01'
    if end is None:
        end = '2023-12-31'
    
    # Fetch data from Yahoo Finance
    stock = yf.Ticker(ticker)
    hist = stock.history(start=start, end=end)
    data = hist.reset_index().to_dict(orient='records')
    
    # Clean the data
    data = clean_data(data)

    # Save the cleaned data to CSV
    save_data_to_csv(data, ticker)
    
    # return response code and not the data
    logging.info(f'Data fetched and saved for ticker: {ticker}')
    return data

# a call to the fetch_stock_data function with a start and end date as an http request
# would look like this:
# http://localhost:5000/data/AAPL?start=2021-01-01&end=2021-12-31

    
# overload fetch_from_storage to accept start and end date
def fetch_from_storage(ticker, start, end):
    csv_path = os.path.join(DATA_DIR, f'{ticker}.csv')
    # add default values for start and end
    if start is None:
        start = '2000-01-01'
    if end is None:
        end = '2023-12-31'
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        # check if the data is within the specified date range and if it is, return it
        # if not, return None
        df['Date'] = pd.to_datetime(df['Date'])
        start = pd.to_datetime(start).tz_localize('UTC')
        end = pd.to_datetime(end).tz_localize('UTC')
        mask = (df['Date'] >= start) & (df['Date'] <= end)
        df = df.loc[mask]
        return df.to_dict(orient='records')
    else:
        return None