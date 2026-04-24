from edgar.controller.edgar_api_controller import EdgarApiController
import pandas as pd
edgar_api_controller = EdgarApiController()
info = edgar_api_controller.get_most_recent_transactions()

# df = pd.read_excel("C:/Users/riley/Desktop/InsiderTrading/edgar/resources/excel_files/output_2026-04-24.xlsx")
# df["test"] = df["transaction_price_per_share"] * df["transaction_shares"]
# print(df["test"])