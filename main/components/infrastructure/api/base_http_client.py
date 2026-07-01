import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class BaseHttpClient:
    def __init__(
        self,
        user_agent=None,
        headers=None,
        rate_limiter=None,
        retries=3,
        backoff_factor=1.5,
        status_forcelist=None,
        timeout=10,
    ):
        self.session = requests.Session()

        if user_agent:
            self.session.headers["User-Agent"] = user_agent

        if headers:
            self.session.headers.update(headers)

        retry = Retry(
            total=retries,
            backoff_factor=backoff_factor,
            status_forcelist=status_forcelist or [500, 502, 503, 504],
            allowed_methods=["GET"],
        )

        adapter = HTTPAdapter(max_retries=retry)

        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)

        self.rate_limiter = rate_limiter
        self.timeout = timeout

        self._lock = threading.Lock()
        self._reset_stats()

    def _reset_stats(self):
        self.completed = 0
        self.success = 0
        self.failed = 0

    def _record_success(self):
        with self._lock:
            self.completed += 1
            self.success += 1

    def _record_failure(self):
        with self._lock:
            self.completed += 1
            self.failed += 1

    def _print_progress(self, total):
        print(
            f"[{self.completed}/{total}] "
            f"Success: {self.success} | Failed: {self.failed}",
            end="\r",
        )

    def get(self, url, **kwargs):
        if self.rate_limiter:
            self.rate_limiter.acquire()

        kwargs.setdefault("timeout", self.timeout)

        return self.session.get(url, **kwargs)

    def fetch(self, url, processor=None):
        """
        Fetch a single URL.

        Returns:
            (url, result)

        If processor is None, returns response.text.
        Otherwise returns processor(response).
        """
        try:
            response = self.get(url)

            if not response.ok:
                self._record_failure()
                return url, None

            self._record_success()

            if processor:
                return url, processor(response)

            return url, response.text

        except requests.RequestException:
            self._record_failure()
            return url, None

    def fetch_all(self, urls, processor=None, max_workers=10, show_progress=True):
        """
        Fetch many URLs concurrently.

        Returns:
            list of processed results.
        """
        if not urls:
            return []

        self._reset_stats()

        results = []
        total = len(urls)

        if show_progress:
            print(f"Fetching {total} objects...\n")

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.fetch, url, processor)
                for url in urls
            ]

            for future in as_completed(futures):
                _, result = future.result()

                if result is not None:
                    results.append(result)

                if show_progress:
                    self._print_progress(total)

        if show_progress:
            print()
            print(
                f"Done. Success: {self.success}, Failed: {self.failed}"
            )

        return results