from datetime import date, datetime, timedelta
import os
from dotenv import load_dotenv
from components.infrastructure.api.base_api_client import BaseApiClient
from components.infrastructure.api.rate_limiter import RateLimiter

load_dotenv()

class EdgarApiBase(BaseApiClient):
    BASE_URL = "https://www.sec.gov/Archives/edgar/daily-index"

    def __init__(self):
        user_agent = os.getenv("SEC_USER_AGENT")

        if not user_agent:
            raise ValueError(
                "SEC_USER_AGENT environment variable is not set."
            )

        super().__init__(
            user_agent,
            rate_limiter=RateLimiter(rate_per_sec=2 / 3),
        )

    def get_last_business_day(self):
        d = datetime.now().date() - timedelta(days=1)
        while d.weekday() >= 5:
            d -= timedelta(days=1)
        return d

    def _get_year_and_quarter(self, date):
        quarter = (date.month - 1) // 3 + 1
        return date.year, f"QTR{quarter}"

    def _build_index_url(self, date):
        year, quarter = self._get_year_and_quarter(date)
        date_str = date.strftime("%Y%m%d")
        return f"{self.BASE_URL}/{year}/{quarter}/master.{date_str}.idx"

    def get_recent_filings_endpoint(self):
        date = self.get_last_business_day()
        return self._build_index_url(date)

    def get_filings_txt_links(self, bulk_link):
        response = self.get(bulk_link)

        if not response or response.status_code != 200:
            return []

        return self._extract_form_links(
            response.text.splitlines(),
            form_type="4"
        )

    def _extract_form_links(self, lines, form_type=None):
        results = []

        for parts in (line.split("|") for line in lines if "|" in line):
            if len(parts) != 5:
                continue

            cik, name, f_type, date_filed, file_path = parts

            if form_type and f_type != form_type:
                continue

            results.append(
                f"https://www.sec.gov/Archives/{file_path}"
            )

        return results

    from datetime import timedelta

    def get_filing_links_by_date_range(self, start_date, end_date, dates_to_exclude):
        current = start_date
        urls = []
    
        # Convert to set for O(1) lookup (important for performance)
        exclude_set = set(dates_to_exclude)
    
        while current <= end_date:
        
            date_str = current.strftime("%Y-%m-%d")  # match your DB format
    
            # Skip weekends + excluded dates
            if current.weekday() < 5 and date_str not in exclude_set:
            
                quarter = (current.month - 1) // 3 + 1
    
                url = (
                    f"https://www.sec.gov/Archives/edgar/daily-index/"
                    f"{current.year}/QTR{quarter}/"
                    f"master.{current.strftime('%Y%m%d')}.idx"
                )
    
                urls.append(url)
    
            current += timedelta(days=1)
    
        return urls