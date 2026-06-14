from alpaca_api.alpaca_api_base import AlpacaApiBase

class AlpacaAccountBase(AlpacaApiBase):
    def __init__(self):
        super().__init__()
        
    def get_account(self):
        account = self.trading_client.get_account()
        return account