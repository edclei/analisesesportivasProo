
# Simple in-memory cache with TTL
import time, threading
_cache = {}
_lock = threading.Lock()

def set(key, value, ttl=15):
    with _lock:
        _cache[key] = (value, time.time() + ttl)

def get(key):
    with _lock:
        v = _cache.get(key)
        if not v:
            return None
        val, exp = v
        if time.time() > exp:
            del _cache[key]
            return None
        return val

def clear():
    with _lock:
        _cache.clear()
