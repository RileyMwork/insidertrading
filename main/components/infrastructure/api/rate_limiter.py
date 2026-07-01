import time
import threading


class RateLimiter:
    def __init__(self, rate_per_sec):
        self.capacity = rate_per_sec
        self.tokens = rate_per_sec
        self.fill_rate = rate_per_sec
        self.timestamp = time.time()
        self.lock = threading.Lock()

    def acquire(self):
        with self.lock:
            now = time.time()
            elapsed = now - self.timestamp
            self.timestamp = now
    
            self.tokens = min(
                self.capacity,
                self.tokens + elapsed * self.fill_rate
            )
    
            if self.tokens < 1:
                sleep_time = (1 - self.tokens) / self.fill_rate
            else:
                sleep_time = 0
                self.tokens -= 1
    
        if sleep_time > 0:
            time.sleep(sleep_time)