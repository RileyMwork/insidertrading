from ..service.edgar_api_service import EdgarApiService
from components.infrastructure.repository.sql.sql_setup import SQLSetup
from components.edgar.repository.edgar_insert import EdgarInsert
from components.edgar.repository.edgar_select import EdgarSelect
from pathlib import Path
from datetime import datetime
import pandas as pd

class EdgarApiController:
    def __init__(self):
        self.edgar_api_service = EdgarApiService()
        self.sql_setup = SQLSetup()
        self.insert_statements = EdgarInsert()
        self.select_statements = EdgarSelect()

    def get_most_recent_transactions(self):

        self.sql_setup.create_edgar_insider_transactions_table()
        most_recent_pull_date = self.select_statements.get_latest_pull_date()
        today = datetime.today().strftime('%Y-%m-%d')
        if most_recent_pull_date == today:
            print("Most Recent Files Already Pulled, Aborting...")
            return
        else:
            print(f"Pulling Files For {today}")
            df = self.edgar_api_service.get_edgar_df()
            full_df = self.map_sic_codes(df)
            self.insert_statements.insert_all_transactions(full_df)
            return full_df
        
    def map_sic_codes(self, df):
        project_root = Path(__file__).resolve().parent.parent.parent

        csv_path = (
            project_root
            / "infrastructure"
            / "resources"
            / "sic_codes_mapped.csv"
        )
    
        other_df = pd.read_csv(csv_path)
    
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
