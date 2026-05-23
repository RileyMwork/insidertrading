from edgar.controller.edgar_api_controller import EdgarApiController
from alpaca_.api.alpaca_api_base import AlpacaApiBase
import pandas as pd

# edgar_api_controller = EdgarApiController()
# info = edgar_api_controller.get_most_recent_transactions()

# df = edgar_api_controller.get_todays_transactions_df()
# print(df["industry"].value_counts())

alpaca_api = AlpacaApiBase(use_paper=True)
account_info = alpaca_api.get_account_info()
print(account_info)