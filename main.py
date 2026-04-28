from edgar.controller.edgar_api_controller import EdgarApiController
from massive.api.massive_api_base import MassiveApiBase
import pandas as pd

edgar_api_controller = EdgarApiController()
info = edgar_api_controller.get_most_recent_transactions()

# df = pd.read_excel("C:/Users/riley/Desktop/InsiderTrading/edgar/resources/excel_files/output_2026-04-27.xlsx")
# x = df[["issuerTradingSymbol", "transaction_code"]].value_counts()
# print(x)

massive_api = MassiveApiBase()
ticker_info = massive_api.get_ticker_overview("AAPL")
print(ticker_info)