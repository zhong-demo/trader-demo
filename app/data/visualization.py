import os
import pandas as pd
import matplotlib.pyplot as plt

def plot_stock_price(ticker):
    csv_path = os.path.join('data', f'{ticker}.csv')
    if not os.path.exists(csv_path):
        return None
    
    df = pd.read_csv(csv_path)
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Close'], label='Close Price')
    plt.xlabel('Date')
    plt.ylabel('Close Price')
    plt.title(f'{ticker} Stock Price')
    plt.legend()
    
    # Save the plot to a file
    plot_path = os.path.join('static', f'{ticker}_price.png')
    plt.savefig(plot_path)
    plt.close()
    
    return plot_path
