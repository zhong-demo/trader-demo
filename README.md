# Trader-backend

This Flask-based API provides historical stock data analysis capabilities.

## Getting Started

1. Install dependencies:

   ```bash
   pip install -r requirements.txt

2. Run the Flask app:

```bash
python run.py

Endpoints
Get Stock Data
URL: /data/<ticker>
Method: GET
Parameters:
ticker: Stock ticker symbol (e.g., AAPL, MSFT)
Response:
JSON object containing historical stock data.
Example
Request:

```bash
curl http://localhost:5000/data/AAPL

Response:

```json
[
  {"Date": "2023-07-16", "Open": 148.56, "High": 150.63, "Low": 148.53, "Close": 150.19, "Volume": 12850000},
  {"Date": "2023-07-17", "Open": 150.21, "High": 152.28, "Low": 149.96, "Close": 151.82, "Volume": 12540000},
  ...
]

Contributing
Feel free to contribute to this project by submitting pull requests or reporting issues.