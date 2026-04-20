import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from infrastructure.api.edgar_api.rate_limiter import RateLimiter


class EdgarTxtFetcher:
    def __init__(self, rate_per_sec=1):
        # ----------------------------
        # HTTP session setup
        # ----------------------------
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Riley Martin rileymartin523@gmail.com",
        })

        retries = Retry(
            total=3,
            backoff_factor=1.5,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )

        adapter = HTTPAdapter(max_retries=retries)
        self.session.mount("https://", adapter)

        # ----------------------------
        # GLOBAL rate limiter (shared across ALL threads)
        # ----------------------------
        self.rate_limiter = RateLimiter(rate_per_sec=rate_per_sec)

        # ----------------------------
        # Thread-safe progress tracking
        # ----------------------------
        self.lock = threading.Lock()
        self.completed = 0
        self.success = 0
        self.failed = 0

    # ----------------------------
    # Single fetch
    # ----------------------------
    def fetch(self, url):
        try:
            # GLOBAL throttling across all threads
            self.rate_limiter.acquire()

            response = self.session.get(url, timeout=10)

            with self.lock:
                self.completed += 1

            if response.status_code == 200:
                with self.lock:
                    self.success += 1
                return url, response.text

            else:
                with self.lock:
                    self.failed += 1
                return url, None

        except Exception:
            with self.lock:
                self.completed += 1
                self.failed += 1
            return url, None

    # ----------------------------
    # Parallel fetch
    # ----------------------------
    def fetch_all(self, urls, max_workers=5):
        results = {}
        total = len(urls)
        if len(urls) == 0:
            print("No Endpoints to Fetch, Quitting Program")
            return
        print(f"Starting download of {total} filings...\n")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.fetch, url): url
                for url in urls
            }

            for future in as_completed(futures):
                url, content = future.result()

                if content:
                    results[url] = content

                print(
                    f"[{self.completed}/{total}] "
                    f"Success: {self.success} | Failed: {self.failed}",
                    end="\r"
                )

        print("\nDone.")
        print(f"Final → Success: {self.success}, Failed: {self.failed}")

        return results