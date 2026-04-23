from ..service.edgar_api_service import EdgarApiService
from ..repository.statements import Statements
from datetime import datetime

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
            self.statements.insert_all_from_df(df)
            return edgar_transactions["output_file_name"]
