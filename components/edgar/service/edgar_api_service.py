from ..api.edgar_api_base import EdgarApiBase
from ..api.edgar_txt_fetcher import EdgarTxtFetcher
from ..api.edgar_txt_file_parser import EdgarTxtFileParser
from components.edgar.repository.edgar_select import EdgarSelect
from datetime import datetime
import pandas as pd

class EdgarApiService:
    def __init__(self):
        self.edgar_api_base = EdgarApiBase()
        self.edgar_txt_fetcher = EdgarTxtFetcher()
        self.edgar_txt_file_parser = EdgarTxtFileParser()
        self.select_statements = EdgarSelect()

    def get_filings_txt_links(self, start_date=None, end_date=None):
        dates_to_exclude = self.select_statements.get_all_distinct_filed_dates()
        if start_date is None and end_date is None:
            bulk_links = [self.edgar_api_base.get_recent_filings_endpoint()]
        else:
            bulk_links = self.edgar_api_base.get_filing_links_by_date_range(start_date, end_date, dates_to_exclude)
        txt_link_list = []
        for bulk_link in bulk_links:
            txt_links = self.edgar_api_base.get_filings_txt_links(bulk_link)
            txt_link_list.append(txt_links)
        return txt_link_list
    
    def get_txt_files(self, txt_link_list):
            txt_files = self.edgar_txt_fetcher.fetch_all(txt_link_list, max_workers=5)
            return txt_files
    
    def get_parsed_data(self, txt_files):
        parent_tag_list = ["issuer", ".//reportingOwnerId",".//reportingOwnerAddress", ".//reportingOwnerRelationship"]

        all_transactions = []
        for txt_file in txt_files:
            filed_date = self.edgar_txt_file_parser.get_txt_field(txt_file, "FILED AS OF DATE")
            converted_file = self.edgar_txt_file_parser.convert_txt_to_xml(txt_file)
            general_info = self.edgar_txt_file_parser.parse_xml_by_parent_tag(converted_file, parent_tag_list)
            non_derivative_transactions = self.edgar_txt_file_parser.parse_xml_non_derivative_table(converted_file)
            non_derivative_transactions_with_general_info = [{**general_info, **txn, "filed_date": filed_date} for txn in non_derivative_transactions]

            all_transactions.extend(non_derivative_transactions_with_general_info)

        return all_transactions
    
    def persist_parsed_data_df_to_sql(self, parsed_data_list):
        df = pd.DataFrame(parsed_data_list)
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
        return df
