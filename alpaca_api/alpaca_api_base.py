import os
from dotenv import load_dotenv
from infrastructure.api.base_api_client import BaseApiClient
from infrastructure.api.rate_limiter import RateLimiter
from alpaca.trading.client import TradingClient

load_dotenv()

class AlpacaApiBase(BaseApiClient):
    BASE_PAPER_URL = "https://paper-api.alpaca.markets/v2/"
    BASE_REAL_URL = "https://api.alpaca.markets/v2/"

    def __init__(self, use_paper=True):
        user_agent = os.getenv("SEC_USER_AGENT")
        api_key = os.getenv("ALPACA_API_KEY")
        api_secret = os.getenv("ALPACA_API_SECRET")
        self. trading_client = TradingClient(api_key, api_secret)

        self.use_paper = use_paper

        if not user_agent:
            raise ValueError(
                "SEC_USER_AGENT environment variable is not set."
            )

        super().__init__(
            user_agent,
            rate_limiter=RateLimiter(rate_per_sec=2 / 3),
        )
        if self.use_paper:
            self.base_url = self.BASE_PAPER_URL
        else:
            self.base_url = self.BASE_REAL_URL
