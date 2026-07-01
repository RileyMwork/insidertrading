from components.alpaca_.api.alpaca_api_base import AlpacaApiBase
from alpaca.data.requests import StockBarsRequest, StockLatestTradeRequest
from alpaca.data.timeframe import TimeFrame

class AlpacaMarketBase(AlpacaApiBase):
    def __init__(self):
        super().__init__()
        
    def get_latest_price(self, ticker):
        request = StockLatestTradeRequest(symbol_or_symbols=ticker)
        response = self.historical_data_client.get_stock_latest_trade(request)
        return response[ticker].price
    
    def get_price_at_time(self, ticker, start_timestamp, end_timestamp):
        request = StockBarsRequest(symbol_or_symbols=ticker, timeframe=TimeFrame.Hour, start=start_timestamp, end=end_timestamp)
        bars = self.historical_data_client.get_stock_bars(request).df
        close_price = bars.iloc[0]["close"]
        return close_price