import re
import json
import urllib
from aiodriver.aiogw import Gameworld
from aiodriver.aioclient import HttpClient
from utilities.response import Response


class Lobby:
    def __init__(self):
        self.client = HttpClient()
        self.api_endpoint = 'https://lobby.kingdoms.com/api/index.php'

    async def authenticate(self, email, password):
        mellon = 'https://mellon-t5.traviangames.com'

        r = await self.client.get(f'{mellon}/authentication/login')
        self.msid = re.search(r'msid=([\w]*)&msname', r).group(1)

        cred = {'email': email, 'password': password}
        r = await self.client.post(
            f'{mellon}/authentication/login/ajax/form-validate?msid={self.msid}&msname=msid',
            payload=cred
        )

        token = re.search(r'token=([\w]*)&msid', r).group(1)
        await self.client.get(
            f'https://lobby.kingdoms.com/api/login.php?token={token}&msid={self.msid}&msname=msid'
        )

        for k in self.client.session.cookie_jar:
            if k.key == 'gl5SessionKey':
                encoded_session = k.value
                break

        decoded_session = urllib.parse.unquote(encoded_session)
        self.session = json.loads(decoded_session)['key']

    async def connect_to_gameworld(self, g_id, g_name):
        gameworld = Gameworld(client=self.client, msid=self.msid)
        await gameworld.authenticate(g_id, g_name)
        return gameworld

    async def post(self, controller, action, params={}, simple_response=True):
        payload = {
            'action': action,
            'controller': controller,
            'params': params,
            'session': self.session
        }
        r = await self.client.post(url=self.api_endpoint, payload=json.dumps(payload))
        if simple_response is True:
            return Response(r)
        return r
