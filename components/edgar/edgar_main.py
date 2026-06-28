from components.edgar.controller.edgar_api_controller import EdgarApiController
from datetime import date, datetime, timedelta

class EdgarMain:
    def __init__(self):
        self.edgar_controller = EdgarApiController()

    def get_transactions(self, start_year, start_month, start_day, end_year, end_month, end_day):
        start_date = date(start_year, start_month, start_day)
        end_date = date(end_year, end_month, end_day)
        return self.edgar_controller.get_transactions(start_date, end_date)

    def get_most_recent_transactions(self, max_days_back=5):
        count = 0
        
        while count < max_days_back:
            now = datetime.now() - timedelta(days=count)

            print(f"Checking for transactions on {now.strftime('%Y-%m-%d')}")

            day = now.day
            month = now.month
            year = now.year

            df = self.edgar_controller.get_transactions(date(year, month, day), date(year, month, day))
            if not df.empty:
                return df
            count += 1

