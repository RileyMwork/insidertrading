from main.components.edgar.repository.insider_transaction_repository import InsiderTransactionRepository
from main.components.infrastructure.api.base_http_client import BaseHttpClient
from main.components.edgar.forms.index_link_builder import IndexLinkBuilder
from main.components.edgar.forms.target_file_parser import TargetFileParser
from main.components.edgar.forms.index_file_parser import IndexFileParser
from main.components.infrastructure.api.rate_limiter import RateLimiter
from dotenv import load_dotenv
import os

load_dotenv()

class EdgarService:
    def __init__(self):
        self.client = BaseHttpClient(user_agent=os.getenv("SEC_USER_AGENT"), rate_limiter=RateLimiter(1), status_forcelist=[429, 500, 502, 503, 504],)
        self.index_builder = IndexLinkBuilder()
        self.index_parser = IndexFileParser()
        self.target_parser = TargetFileParser()
        self.insider_transaction_repository = InsiderTransactionRepository()


    def get_index_files(self, start_date : str, end_date : str) -> list[str]:
        exclude_dates = self.insider_transaction_repository.get_all_distinct_filed_dates()

        urls = self.index_builder.build_index_links(start_date, end_date, exclude_dates)

        return self.client.fetch_all(urls)
    
    def get_filing_links(self, index_files : list[str], form_type : str = "4") -> list[str]:
        all_links = []

        for file_text in index_files:
            links = self.index_parser.extract_form_links(file_text, form_type=form_type)
            all_links.extend(links)

        return all_links
    
    def get_filings(self, filing_urls : list[str]) -> list[str]:
        return self.client.fetch_all(filing_urls)
    
    def parse_transactions(self, filings : list[str]) -> list[dict[str, str | None]]:
        all_transactions = []

        for txt in filings:
            xml = self.target_parser.convert_txt_to_xml(txt)

            if not xml:
                continue

            filed_date = self.target_parser.get_txt_field(txt, "FILED AS OF DATE")

            transactions = self.target_parser.parse_xml_non_derivative_table(xml)

            for tx in transactions:
                tx["filed_date"] = filed_date
                
            all_transactions.extend(transactions)

        return all_transactions
    
    def get_transactions(self, start_date : str, end_date : str, form_type : str = "4") -> list[dict[str, str | None]]:
        index_files = self.get_index_files(start_date, end_date)

        filing_links = self.get_filing_links(index_files, form_type=form_type)

        filings = self.get_filings(filing_links)

        return self.parse_transactions(filings)