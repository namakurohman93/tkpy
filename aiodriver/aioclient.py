import aiohttp


class UnknownContentType(Exception):
    """ debug purpose when content-type neither text & json """


class HttpClient:
    def __init__(self):
        self.headers = {
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:65.0) Gecko/20100101 Firefox/65.0'
        }
        self.session = aiohttp.ClientSession(headers=self.headers)

    async def post(self, url, payload={}):
        self.response = await self.session.post(url, data=payload)
        r = await self.return_response()
        return r

    async def get(self, url):
        self.response = await self.session.get(url)
        r = await self.return_response()
        return r

    async def return_response(self):
        if 'text' in self.response.headers['content-type']:
            return await self.response.text()
        elif 'json' in self.response.headers['content-type']:
            return await self.response.json()
        else:
            raise UnknownContentType(self.response.headers['content-type'])

    async def close(self):
        await self.session.close()
