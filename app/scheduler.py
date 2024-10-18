from apscheduler.schedulers.background import BackgroundScheduler
from .data.update_data import update_csv_files

def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # List of ticker symbols to update
    tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN']  # Add more tickers as needed
    
    # Schedule the update function to run daily
    scheduler.add_job(update_csv_files, 'interval', days=1, args=[tickers])
    
    scheduler.start()
    print('Scheduler started')
