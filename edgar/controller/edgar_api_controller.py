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

        self.statements.create_table();
        most_recent_pull_date = self.statements.get_latest_pull_date()
        today = datetime.today().strftime('%Y-%m-%d')
        if most_recent_pull_date == today:
            print("Most Recent Files Already Pulled, Aborting...")
            return
        else:
            print(f"Pulling Files For {today}")
            df = self.edgar_api_service.get_edgar_df()
            full_df = self.map_sic_codes(df)
            self.statements.insert_all_from_df(full_df)
            return full_df
        
    def map_sic_codes(self, df):
        base_dir = Path(__file__).resolve().parent.parent
        csv_path = base_dir / "resources" / "sic_codes_mapped.csv"
    
        print(csv_path)  # optional debug
    
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
