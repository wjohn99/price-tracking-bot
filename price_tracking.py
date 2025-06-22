from dotenv import load_dotenv
import os
import requests

load_dotenv()
API_KEY = os.environ['API_KEY']
API_ENDPOINT = 'https://api.coingecko.com/api/v3/simple/price'

class PriceTracking:
    def __init__(self):
        self.header = {
            "x-cg-pro-api-key": API_KEY
        }

    def get_coin_price(self, coin_id):
        self.params = {
            'ids': coin_id,
            'vs_currencies': 'usd'
        }

        r = requests.get(API_ENDPOINT, headers=self.header, params=self.params)
        return r.json()[coin_id]['usd']