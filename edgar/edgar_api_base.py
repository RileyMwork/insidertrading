from datetime import datetime, timedelta, timezone
from infrastructure.api.edgar_api.base_api_client import BaseApiClient
from infrastructure.api.edgar_api.rate_limiter import RateLimiter


class EdgarApiBase(BaseApiClient):
    def __init__(self):
        super().__init__(
            "Riley Martin rileymartin523@gmail.com",
            rate_limiter=RateLimiter(rate_per_sec=1/3)
        )

    def get_last_business_day(self):
        d = datetime.now(timezone.utc).date() - timedelta(days=1)

        while d.weekday() >= 5:
            d -= timedelta(days=1)

        return d

    def get_recent_filings_txt_links(self):
        date = self.get_last_business_day()
        date_str = date.strftime("%Y%m%d")

        url = f"https://www.sec.gov/Archives/edgar/daily-index/2026/QTR2/master.{date_str}.idx"
        print(f"Checking: {url}")

        response = self.get(url)

        if response and response.status_code == 200:
            print("Succesfully Retrieved Endpoints")
            return self.parse(response.text.splitlines())
        else:
            print(f"Could Not Retrieve Endpoints, Response Status Code: {response.status_code}")
            return []

    def parse(self, lines):
        results = []

        for line in lines:
            if "|" not in line:
                continue

            parts = line.split("|")
            if len(parts) != 5:
                continue

            cik, name, form_type, date_filed, file_path = parts

            if form_type == "4":
                results.append(f"https://www.sec.gov/Archives/{file_path}")

        print(f"Found {len(results)} .txt links")
        return results