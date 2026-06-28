from datetime import datetime, timedelta
from ..service.edgar_api_service import EdgarApiService
from components.infrastructure.repository.sql.sql_setup import SQLSetup
from components.edgar.repository.edgar_insert import EdgarInsert
from components.edgar.repository.edgar_select import EdgarSelect
from pathlib import Path
import pandas as pd

class EdgarApiController:
    def __init__(self):
        self.edgar_api_service = EdgarApiService()
        self.sql_setup = SQLSetup()
        self.insert_statements = EdgarInsert()

    def get_transactions(self, start_date=None, end_date=None):

        txt_link_lists = self.edgar_api_service.get_filings_txt_links(start_date, end_date)

        all_dfs = []

        print(f"Processing {len(txt_link_lists)} trading days")

        for day_num, txt_link_list in enumerate( txt_link_lists, start=1):
            print(f"Day {day_num}: "f"{len(txt_link_list)} Form 4 filings")

            if not txt_link_list:
                print("No filings found")
                continue

            txt_files = self.edgar_api_service.get_txt_files(txt_link_list)

            parsed_data = self.edgar_api_service.get_parsed_data(txt_files)

            if not parsed_data:
                print("No transactions parsed")
                continue

            df = self.edgar_api_service.persist_parsed_data_df_to_sql(parsed_data)

            full_df = self.map_sic_codes(df)

            self.insert_statements.insert_all_transactions(full_df)

            print(f"Inserted {len(full_df)} transactions")

            all_dfs.append(full_df)

        if all_dfs:
            return pd.concat(all_dfs, ignore_index=True)

        return pd.DataFrame()
        

    def map_sic_codes(self, df):
        project_root = (Path(__file__).resolve().parent.parent.parent)

        csv_path = (project_root/"infrastructure"/"resources"/"sic_codes_mapped.csv"
        )

        other_df = pd.read_csv(csv_path)

        other_df["ticker"] = (other_df["ticker"].str.strip("[]'"))

        other_df = other_df[["ticker", "sic", "industry"]]

        merged = df.merge(other_df, left_on="issuerTradingSymbol", right_on="ticker", how="left")

        merged = merged.drop(columns=["ticker"])

        return merged