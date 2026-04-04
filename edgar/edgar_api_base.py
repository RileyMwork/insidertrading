from bs4 import BeautifulSoup
import requests

class EdgarApiBase:
    def __init__(self):
        self.base_url = f"https://www.sec.gov/cgi-bin/browse-edgar?action=getcurrent&type=4&"
        self.headers = {
            "User-Agent": "Riley Martin rileymartin523@gmail.com",
        }
    
    def get_recent_filings_txt_file_links(self, filing_type="4", count=100, start=0):

        full_url = self.base_url + f"type={filing_type}&count={count}&output=atom&start={start}"
        response = requests.get(full_url, headers=self.headers)

        soup = BeautifulSoup(response.content, "xml")
        
        entries = soup.find_all("entry")
        
        links = []
        for e in entries:
            link_tag = e.find("link", {"rel": "alternate"})
            if link_tag and link_tag.has_attr("href"):
                href = link_tag["href"]
                formatted_href = href.replace("-index.htm", ".txt")
                links.append(formatted_href)

        return links
    
    def get_recent_filings_txt_file_links_loop(self, filing_type="4", count=100, start=0, end=500):
        links_agg = []
        while start < end:
            links = self.get_recent_filings_txt_file_links(filing_type=filing_type, count=count, start=start)
            for link in links:
                links_agg.append(link)
            start += 100
        return links_agg