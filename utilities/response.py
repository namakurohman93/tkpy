class Response:
    def __init__(self, response):
        self._raw = response
        self._cache()
        del response

    def __iter__(self):
        return iter(map(Cache, (d['data'] for d in self.cache)))

    def __repr__(self):
        return str(self.cache)

    def _cache(self):
        try:
            self.cache = self._raw['cache'][0]['data']['cache']
        except:
            self.cache = self._raw['response']


class Cache:
    """get dict value through attribute"""
    def __init__(self, cache):
        self.cache = cache

    def __getattr__(self, key):
        return self.cache[key]
