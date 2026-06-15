import json
import hashlib

class RedisCache:
    def __init__(self):
        # Mocking Redis for this prototype
        self.cache = {}

    def _generate_key(self, query: str) -> str:
        return hashlib.md5(query.encode()).hexdigest()

    def get(self, query: str) -> str:
        key = self._generate_key(query)
        return self.cache.get(key)

    def set(self, query: str, answer: str):
        key = self._generate_key(query)
        self.cache[key] = answer
