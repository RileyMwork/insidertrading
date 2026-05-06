from ..api.edgar_api_base import EdgarApiBase
from ..api.edgar_txt_fetcher import EdgarTxtFetcher
from ..api.edgar_txt_file_parser import EdgarTxtFileParser
from datetime import datetime
import pandas as pd

class EdgarApiService:
    def __init__(self):
        self.edgar_api_base = EdgarApiBase()
        self.edgar_txt_fetcher = EdgarTxtFetcher()
        self.edgar_txt_file_parser = EdgarTxtFileParser()

    def get_edgar_df(self):
        txt_links = self.edgar_api_base.get_recent_filings_txt_links()
        txt_files = self.edgar_txt_fetcher.fetch_all(txt_links, max_workers=5)

        parent_tag_list = ["issuer", ".//reportingOwnerId",".//reportingOwnerAddress", ".//reportingOwnerRelationship"]

        all_transactions = []
        for txt_file in txt_files:
            converted_file = self.edgar_txt_file_parser.convert_txt_to_xml(txt_file)
            general_info = self.edgar_txt_file_parser.parse_xml_by_parent_tag(converted_file, parent_tag_list)
            non_derivative_transactions = self.edgar_txt_file_parser.parse_xml_non_derivative_table(converted_file)
            non_derivative_transactions_with_general_info = [{**general_info, **txn} for txn in non_derivative_transactions]

            all_transactions.extend(non_derivative_transactions_with_general_info)

        df = pd.DataFrame(all_transactions)
        today = datetime.today().strftime('%Y-%m-%d')
        df["date_pulled_from_edgar"] = today
        bool_map = {
                1: True, 0: False,
                "1": True, "0": False,
                True: True, False: False,
                "True": True, "False": False,
                "true": True, "false": False,
            }
        cols = ["isDirector", "isOfficer", "isTenPercentOwner", "isOther"]
        df[cols] = (df[cols].replace(bool_map).fillna(False).astype(bool))
        df["transaction_shares"] = pd.to_numeric(df["transaction_shares"], errors="coerce").fillna(0)
        df["transaction_price_per_share"] = pd.to_numeric(df["transaction_price_per_share"], errors="coerce").fillna(0)
        df["total_transaction_cost"] = df["transaction_shares"] * df["transaction_price_per_share"]
        output_file_name = f"output_{today}.xlsx"
        return {"df": df, "output_file_name": output_file_name}
