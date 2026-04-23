from datetime import datetime, timedelta, timezone
from .base_api_client import BaseApiClient
from .rate_limiter import RateLimiter


class EdgarApiBase(BaseApiClient):
    BASE_URL = "https://www.sec.gov/Archives/edgar/daily-index"

    def __init__(self):
        super().__init__(
            "Riley Martin rileymartin523@gmail.com",
            rate_limiter=RateLimiter(rate_per_sec=1 / 3),
        )

    def get_last_business_day(self):
        d = datetime.now().date() - timedelta(days=1)
        while d.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            d -= timedelta(days=1)
        return d

    def _get_year_and_quarter(self, date):
        quarter = (date.month - 1) // 3 + 1
        return date.year, f"QTR{quarter}"

    def _build_index_url(self, date):
        year, quarter = self._get_year_and_quarter(date)
        date_str = date.strftime("%Y%m%d")
        print()
        return f"{self.BASE_URL}/{year}/{quarter}/master.{date_str}.idx"

    def get_recent_filings_txt_links(self):
        date = self.get_last_business_day()
        url = self._build_index_url(date)
        print(url)
        response = self.get(url)
        if not response or response.status_code != 200:
            return []

        return self._extract_form_links(response.text.splitlines(), form_type="4")

    def _extract_form_links(self, lines, form_type=None):
        results = []

        for parts in (line.split("|") for line in lines if "|" in line):
            if len(parts) != 5:
                continue

            cik, name, f_type, date_filed, file_path = parts

            if form_type and f_type != form_type:
                continue

            results.append(f"https://www.sec.gov/Archives/{file_path}")

        return results