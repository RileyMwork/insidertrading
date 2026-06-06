from alpaca_.api.alpaca_api_base import AlpacaApiBase
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass, AssetStatus

class AlpacaPositionsBase(AlpacaApiBase):
    def __init__(self):
        super().__init__()

    def get_all_positions(self):
        positions = self.trading_client.get_all_positions()
        return positions

    def get_position(self, ticker):
        position = self.trading_client.get_open_position(ticker)
        return position