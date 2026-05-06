from edgar.controller.edgar_api_controller import EdgarApiController
import pandas as pd

edgar_api_controller = EdgarApiController()
info = edgar_api_controller.get_most_recent_transactions()

df = edgar_api_controller.get_todays_transactions_df()
print(df["industry"].value_counts())
