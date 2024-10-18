import unittest
from app import create_app
import os

class StockAnalysisAPITestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), "Welcome to the Trader.win API")

    def test_valid_ticker(self):
        response = self.client.get('/data/AAPL')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Date', response.json[0])
        self.assertIn('Close', response.json[0])

    def test_data_saved_to_csv(self):
        ticker = 'AAPL'
        self.client.get(f'/data/{ticker}')
        csv_path = os.path.join('./app/data/tickers', f'{ticker}.csv')
        self.assertTrue(os.path.exists(csv_path))

    def test_load_data_from_csv(self):
        ticker = 'AAPL'
        self.client.get(f'/data/{ticker}')
        # Now delete data from memory and force reload from CSV
        from app.data.storage import load_data_from_csv
        data = load_data_from_csv(ticker)
        self.assertIsNotNone(data)

    def test_data_cleaning(self):
        ticker = 'AAPL'
        response = self.client.get(f'/data/{ticker}')
        # Assuming clean_data removes rows with missing values
        from app.data.process_data import clean_data
        raw_data = response.json
        cleaned_data = clean_data(raw_data)
        self.assertEqual(len(cleaned_data), len(raw_data))

    def test_caching_mechanism(self):
        ticker = 'AAPL'
        response_first = self.client.get(f'/data/{ticker}')
        response_second = self.client.get(f'/data/{ticker}')
        self.assertEqual(response_first.data, response_second.data)

    def test_documentation_endpoint(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Welcome to the Trader.win API", response.data.decode('utf-8'))

if __name__ == '__main__':
    unittest.main()
