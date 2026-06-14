from alpaca_api.alpaca_api_base import AlpacaApiBase
from alpaca.data.requests import StockLatestTradeRequest

class AlpacaMarketBase(AlpacaApiBase):
    def __init__(self):
        super().__init__()
        
    def get_latest_price(self, ticker):
        request = StockLatestTradeRequest(symbol_or_symbols=ticker)
        response = self.historical_data_client.get_stock_latest_trade(request)
        return response[ticker].price