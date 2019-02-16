import re
import json
import time
import urllib
from utilities.response import Response


class Gameworld:
    def __init__(self, client, msid):
        self.client = client
        self.msid = msid
        self.api_endpoint = 'https://{}.kingdoms.com/api/?'

    async def authenticate(self, gameworld_id, gameworld_name):
        mellon = 'https://mellon-t5.traviangames.com'

        r = await self.client.get(
            f'{mellon}/game-world/join/gameWorldId/{gameworld_id}?msid={self.msid}&msname=msid'
        )

        token = re.search(r'token=([\w]*)&msid', r).group(1)
        await self.client.get(
            f'https://{gameworld_name.lower()}.kingdoms.com/api/login.php?token={token}&msid={self.msid}&msname=msid'
        )

        for k in self.client.session.cookie_jar:
            if k.key == 't5SessionKey':
                encoded_session = k.value
                break

        # attribute error, cookiejar has no attribute get
        # encoded_session = self.client.session.cookie_jar.get('t5SessionKey')

        decoded_session = urllib.parse.unquote(encoded_session)
        self.session = json.loads(decoded_session)['key']
        self.player_id = json.loads(decoded_session)['id']

        self.api_endpoint = self.api_endpoint.format(gameworld_name.lower())

    async def post(self, controller, action, params={}, simple_response=True):
        payload = {
            'action': action,
            'controller': controller,
            'params': params,
            'session': self.session
        }

        timestamp = int('{:.2f}'.format(time.time()).replace('.', ''))
        url = f'{self.api_endpoint}c={controller}&a={action}&t{timestamp}'

        r = await self.client.post(url, payload=json.dumps(payload))

        if simple_response is True:
            return Response(r)
        return r
