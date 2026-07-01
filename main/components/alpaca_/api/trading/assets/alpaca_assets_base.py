from components.alpaca_.api.alpaca_api_base import AlpacaApiBase
from alpaca.trading.requests import GetAssetsRequest
from alpaca.trading.enums import AssetClass, AssetStatus

class AlpacaAssetsBase(AlpacaApiBase):
    def __init__(self):
        super().__init__()

    def get_assets(self):
        search_params = GetAssetsRequest(asset_class=AssetClass.US_EQUITY, status=AssetStatus.ACTIVE)
        assets = self.trading_client.get_all_assets(search_params)

        tradeable_assets = [asset for asset in assets if asset.tradable]

        return tradeable_assets