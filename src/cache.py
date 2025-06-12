import time
from collections import OrderedDict
import threading

class Cache:
    def __init__(self):
        self.ttl = 3600
        self.cache = OrderedDict()
        self._lock = threading.RLock()

    def _cleanup_expired(self):
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self.cache.items()
            if expiry < current_time
        ]
        for key in expired_keys:
            del self.cache[key]

    def get(self, key):
        with self._lock:
            self._cleanup_expired()
            if key in self.cache:
                value, expiry = self.cache[key]
                if expiry > time.time():
                    self.cache.move_to_end(key)
                    return value
                else:
                    del self.cache[key]
            return None

    def set(self, key, value):
        with self._lock:
            expiry_time = time.time() + self.ttl
            self.cache[key] = (value, expiry_time)
            self.cache.move_to_end(key)

    def clear(self):
        with self._lock:
            self.cache.clear()