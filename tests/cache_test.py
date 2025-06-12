import pytest
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.cache import Cache


def test_cache_set_and_get():
    cache = Cache()
    cache.set("key1", "value1")
    assert cache.get("key1") == "value1"


def test_cache_get_nonexistent():
    cache = Cache()
    assert cache.get("nonexistent") is None


def test_cache_expiry():
    cache = Cache()
    cache.ttl = 1
    cache.set("key1", "value1")
    time.sleep(1.1)
    assert cache.get("key1") is None


def test_cache_clear():
    cache = Cache()
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.clear()
    assert cache.get("key1") is None
    assert cache.get("key2") is None


def test_cache_cleanup_expired():
    cache = Cache()
    cache.ttl = 1
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    time.sleep(1.1)
    cache._cleanup_expired()
    assert len(cache.cache) == 0


def test_cache_update_existing():
    cache = Cache()
    cache.set("key1", "value1")
    cache.set("key1", "value2")
    assert cache.get("key1") == "value2"


def test_cache_multiple_keys():
    cache = Cache()
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    assert cache.get("key1") == "value1"
    assert cache.get("key2") == "value2" 