from main.components.edgar.repository.insider_transaction_repository import InsiderTransactionRepository
from ..service.edgar_service import EdgarService
import pandas as pd

class EdgarController:
    def __init__(self):
        self.edgar_service = EdgarService()
        self.repo = InsiderTransactionRepository()

    def get_transactions(self, start_date : str, end_date : str) -> pd.DataFrame:

        parsed_data = self.edgar_service.get_transactions(start_date, end_date)

        if not parsed_data:
            print("No transactions found")
            return pd.DataFrame()

        df = pd.DataFrame(parsed_data)

        self.repo.insert_all_transactions(df)

        print(f"Inserted {len(df)} transactions")

        return df
