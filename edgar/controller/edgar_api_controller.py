from ..service.edgar_api_service import EdgarApiService
from ..repository.statements import Statements
from pathlib import Path
from datetime import datetime
import pandas as pd

class EdgarApiController:
    def __init__(self):
        self.edgar_api_service = EdgarApiService()
        self.statements = Statements()

    def get_most_recent_transactions(self):
        most_recent_pull_date = self.statements.get_latest_pull_date()
        today = datetime.today().strftime('%Y-%m-%d')
        if most_recent_pull_date == today:
            print("Most Recent Files Already Pulled, Aborting...")
            return
        else:
            print(f"Pulling Files For {today}")
            edgar_transactions = self.edgar_api_service.get_edgar_df()
            df = edgar_transactions["df"]
            full_df = self.map_sic_codes(df)
            self.statements.insert_all_from_df(full_df)
            output_file_name = f"output_{today}.xlsx"
            full_df.to_excel(f"edgar/resources/excel_files/{output_file_name}")
            return full_df
        
    def map_sic_codes(self, df):
        other_df = pd.read_csv("C:\\Users\\riley\\Desktop\\InsiderTrading\\edgar\\resources\\sic_codes_mapped.csv")
        other_df["ticker"] = other_df["ticker"].str.strip("[]'")
        other_df = other_df[["ticker", "sic", "industry"]]
        
        merged = df.merge(
            other_df,
            left_on="issuerTradingSymbol",
            right_on="ticker",
            how="left"
        )
        
        merged = merged.drop(columns=["ticker"])
        return merged
    
    def get_todays_transactions_df(self):
        folder = Path("edgar/resources/excel_files")

        files = list(folder.glob("output_*.xlsx"))

        latest_file = max(
            files,
            key=lambda f: datetime.strptime(
                f.stem.replace("output_", ""),
                "%Y-%m-%d"
            )
        )
        df = pd.read_excel(latest_file)
        return df
