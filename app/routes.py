from flask import Blueprint, jsonify, request
from .data.fetch_data import fetch_stock_data, fetch_from_storage
from .data.process_data import clean_data
import pandas as pd
import logging

main = Blueprint('main', __name__)

@main.route('/')
def index():
    logging.info('Index route accessed.')
    return "Welcome to the Trader.win API"

@main.route('/data/<ticker>', methods=['GET'])
def get_stock_data(ticker):
    logging.info(f'Request received for ticker: {ticker}')
    # get start and end date from query parameters
    start = request.args.get('start')
    end = request.args.get('end')
    try:
        data = fetch_stock_data(ticker, start, end)
        if not data:
            logging.warning(f'No data found for ticker: {ticker}')
            abort(400, description=f"No data found for ticker '{ticker}'")
        return jsonify(data)
    except Exception as e:
        logging.error(f'Error fetching data for ticker {ticker}: {e}')
        abort(400, description=str(e))

@main.errorhandler(Exception)
def handle_server_error(e):
    return jsonify(error=str(e)), 500

@main.errorhandler(404)
def handle_not_found_error(e):
    return jsonify(error=str(e)), 404

@main.errorhandler(400)
def handle_bad_request_error(e):
    return jsonify(error=str(e)), 400

@main.errorhandler(405)
def handle_method_not_allowed_error(e):
    return jsonify(error=str(e)), 405

def is_valid_ticker(ticker):
    # Implement your validation logic here
    # Example: Check if the ticker exists in a predefined list or API
    valid_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
    return ticker.upper() in valid_tickers

def abort(status_code, description=None):
    raise Exception(description)

# route to clean up the data
@main.route('/clean/<ticker>', methods=['GET'])
def clean_stock_data(ticker):
    try:
        data = fetch_from_storage(ticker)
        if not data:
            abort(404, description=f"No data found for ticker '{ticker}'")
        cleaned_data = clean_data(data)
        # save
        df = pd.DataFrame(cleaned_data)
        df.to_csv(f'./app/data/tickers/{ticker}_cleaned.csv', index=False)
        # return response code and not the data
        return '', 204
    except Exception as e:
        abort(500, description=str(e))

# route to fetch the cleaned data
@main.route('/cleaned_data/<ticker>', methods=['GET'])
def get_cleaned_stock_data(ticker):
    try:
        csv_path = f'./app/data/tickers/{ticker}_cleaned.csv'
        if not os.path.exists(csv_path):
            abort(404, description=f"No cleaned data found for ticker '{ticker}'")
        # return response code and not the data
        return '', 204
    except Exception as e:
        abort(500, description=str(e))

