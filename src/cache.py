import time
from typing import Optional, Dict, Tuple
from settings import Settings

class Cache:
    def __init__(self):
        self.settings = Settings()
        self.memory_cache: Dict[str, Tuple[str, float]] = {}  # key -> (value, expiry_time)
        self.ttl = self.settings.cache_ttl
        print("Using in-memory cache")

    def ping(self) -> bool:
        """
        Check if cache is available (always true for in-memory)
        """
        return True

    def _cleanup_memory_cache(self):
        """
        Remove expired entries from memory cache
        """
        current_time = time.time()
        expired_keys = [
            key for key, (_, expiry) in self.memory_cache.items()
            if expiry < current_time
        ]
        for key in expired_keys:
            del self.memory_cache[key]

    def get(self, key: str) -> Optional[str]:
        """
        Get value from cache
        """
        self._cleanup_memory_cache()
        if key in self.memory_cache:
            value, expiry = self.memory_cache[key]
            if expiry > time.time():
                return value
            else:
                del self.memory_cache[key]
        return None

    def set(self, key: str, value: str) -> bool:
        """
        Set value in cache with TTL
        """
        expiry_time = time.time() + self.ttl
        self.memory_cache[key] = (value, expiry_time)
        return True

    def delete(self, key: str) -> bool:
        """
        Delete value from cache
        """
        if key in self.memory_cache:
            del self.memory_cache[key]
            return True
        return False

    def clear(self) -> bool:
        """
        Clear all cache entries
        """
        self.memory_cache.clear()
        return True
    
    def get_stats(self) -> dict:
        """
        Get cache statistics
        """
        self._cleanup_memory_cache()
        return {
            "type": "memory",
            "entries": len(self.memory_cache),
            "ttl": self.ttl
        }