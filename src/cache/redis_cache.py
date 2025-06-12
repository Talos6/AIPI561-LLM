import redis
import json
from config.settings import Settings

class RedisCache:
    def __init__(self):
        self.settings = Settings()
        self.redis_client = redis.Redis(
            host=self.settings.redis_host,
            port=self.settings.redis_port,
            password=self.settings.redis_password,
            decode_responses=True
        )
        self.ttl = self.settings.cache_ttl

    def get(self, key: str) -> str:
        """
        Get value from cache
        """
        try:
            return self.redis_client.get(key)
        except redis.RedisError:
            return None

    def set(self, key: str, value: str) -> bool:
        """
        Set value in cache with TTL
        """
        try:
            return self.redis_client.setex(key, self.ttl, value)
        except redis.RedisError:
            return False

    def delete(self, key: str) -> bool:
        """
        Delete value from cache
        """
        try:
            return self.redis_client.delete(key) > 0
        except redis.RedisError:
            return False