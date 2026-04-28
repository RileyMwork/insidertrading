from .base_api_client import BaseApiClient
from .rate_limiter import RateLimiter
import requests

class MassiveApiBase(BaseApiClient):
    BASE_URL = "https://api.massive.com/v3/reference/"

    def __init__(self):
        super().__init__(
            "Riley Martin rileymartin523@gmail.com",
            rate_limiter=RateLimiter(rate_per_sec=1 / 3),
        )
        self.massive_api_key = "YT432XybRLVqCCv363dCfOUQJO3ZoUC4"

    def get_ticker_overview(self, ticker):
        url = f"{self.BASE_URL}tickers/{ticker}?apiKey={self.massive_api_key}"

        response = self.get(url)

        if (response.status_code == 200):
            return response.text
        else:
            print(f"Massive Response Status Code: {response.status_code}")