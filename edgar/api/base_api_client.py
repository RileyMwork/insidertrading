import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseApiClient:
    def __init__(self, user_agent, rate_limiter=None):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": user_agent})

        retries = Retry(
            total=3,
            backoff_factor=1.5,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        self.session.mount("https://", HTTPAdapter(max_retries=retries))

        self.rate_limiter = rate_limiter

    def get(self, url, **kwargs):
        if self.rate_limiter:
            self.rate_limiter.acquire()

        return self.session.get(url, **kwargs)