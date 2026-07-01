from datetime import timedelta, date, datetime

class IndexLinkBuilder():
    def __init__(self):
        self.base_url = "https://www.sec.gov/Archives/edgar/daily-index"

    def build_index_links(self, start_date : str, end_date : str, dates_to_exclude : list[str]) -> list[str]:
        def normalize(d : str) -> date:
            if isinstance(d, date):
                return d
            return datetime.strptime(d, "%Y-%m-%d").date()
    
        start_date = normalize(start_date)
        end_date = normalize(end_date)
    
        exclude_set = {normalize(d) if not isinstance(d, date) else d for d in dates_to_exclude}
    
        current = start_date
        urls = []
    
        while current <= end_date:
        
            if current.weekday() < 5 and current not in exclude_set:
            
                quarter = (current.month - 1) // 3 + 1
    
                url = (
                    f"https://www.sec.gov/Archives/edgar/daily-index/"
                    f"{current.year}/QTR{quarter}/"
                    f"master.{current.strftime('%Y%m%d')}.idx"
                )
    
                urls.append(url)
    
            current += timedelta(days=1)
    
        return urls
