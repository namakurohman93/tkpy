class Response:
    def __init__(self, response):
        self._response = response
        self._check_response()
        del response

    def __getattr__(self, key):
        return self.cache[key]

    def __iter__(self):
        try:
            # return iter(map(Cache, (d['data'] for d in self.cache)))
            return iter(map(Cache, map(lambda d: d['data'], self.cache)))
        except:
            return iter(list(self.cache.keys()))

    def __repr__(self):
        return str(self.cache)

    def _check_response(self):
        if 'cache' in self._response['cache'][0]['data']:
            self.cache = self._response['cache'][0]['data']['cache']
        else:
            self.cache = self._response['response'] or self._response['cache'][0]['data']


class Cache:
    """get dict value through attribute"""
    def __init__(self, cache):
        self._cache = cache

    def __getattr__(self, key):
        return self._cache[key]
