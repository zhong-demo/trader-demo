import os
import pandas as pd

def save_data_to_csv(data, ticker):
    df = pd.DataFrame(data)
    # print current working directory
    print(os.getcwd())
    csv_path = os.path.join('./app/data/tickers', f'{ticker}.csv')
    df.to_csv(csv_path, index=False)

def load_data_from_csv(ticker):
    csv_path = os.path.join('./app/data/tickers', f'{ticker}.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        print(df.columns)
        return df.to_dict(orient='records')
    else:
        return None