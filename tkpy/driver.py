import json
import time
import requests
from urllib import parse
from .exception import NotAuthenticated, AvatarNotFound
from primordial.controllers.lobby import (
    achievements, cache, dual, gameworld, notification, player, sitter, login
)
from primordial.controllers.gameworld import (
    player, farmList, logger, troops, village, cache, quest, error, auctions,
    hero, building, trade, ranking, kingdom, map, reports, society,
    premiumFeature, payment, kingdomTreaty, login
)


class HttpClient:
    def __init__(self, cookies=None):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0'}
        self.cookies = self._set_cookies(cookies)
        self.timeout = 20
        self.hooks = {'response': (self._update_cookies,)}

    def post(self, url, **kwargs):
        return self._request('POST', url, **kwargs)

    def get(self, url, **kwargs):
        return self._request('GET', url, **kwargs)

    def _request(self, method, url, **kwargs):
        for kwarg in ['headers', 'cookies', 'timeout', 'hooks']:
            if kwarg in kwargs:
                kwargs.pop(kwarg)
        with requests.request(
                method=method,
                url=url,
                headers=self.headers,
                cookies=self.cookies,
                timeout=self.timeout,
                hooks=self.hooks,
                **kwargs) as r:
            return r

    def _update_cookies(self, r, *args, **kwargs):
        self.cookies.update(r.cookies)

    def _set_cookies(self, cookies):
        cookie_jar = requests.cookies.RequestsCookieJar()
        if cookies:
            xs = {
                'msid': '.kingdoms.com',
                'gl5SessionKey': 'lobby.kingdoms.com',
                'gl5PlayerId': 'lobby.kingdoms.com',
                'gameworld': 'www.example.com',
                't5SessionKey': f'{cookies["gameworld"]}.kingdoms.com',
                't5mu': f'{cookies["gameworld"]}.kingdoms.com'
            }
            for x in xs:
                cookie_jar.set(
                    name=x,
                    value=cookies[x],
                    domain=xs[x]
                )
        return cookie_jar

    def get_cookie(self, name, domain=None):
        return self.cookies.get(name=name, domain=domain)


class Lobby:
    api_root = 'https://lobby.kingdoms.com/api/index.php'

    def __init__(self, cookies=None):
        self.client = HttpClient(cookies)

        self.achievements = achievements.Achievements(post_handler=self.post)
        self.cache = cache.Cache(post_handler=self.post)
        self.dual = dual.Dual(post_handler=self.post)
        self.gameworld = gameworld.Gameworld(post_handler=self.post)
        self.login = login.Login(post_handler=self.post)
        self.notification = notification.Notification(post_handler=self.post)
        self.player = player.Player(post_handler=self.post)
        self.sitter = sitter.Sitter(post_handler=self.post)

    def is_authenticated(self):
        if 'error' in self.gameworld.getPossibleNewGameworlds():
            raise NotAuthenticated()

    def authenticate(self, email, password):
        mellon_url = 'https://mellon-t5.traviangames.com'
        r = self.client.get(f'{mellon_url}/authentication/login')
        msid = r.text[r.text.find('msid=')+5: r.text.find('msid=')+31]
        r = self.client.post(
            f'{mellon_url}/authentication/login/ajax/form-validate?msid={msid}&msname=msid',
            data={
                'email': email,
                'password': password
            }
        )
        token = r.text[r.text.find('token=')+6: r.text.find('token=')+38]
        self.client.get(
            f'https://lobby.kingdoms.com/api/login.php?token={token}&msid={msid}&msname=msid'
        )
        self.client.cookies.set(
            name='msid',
            value=msid,
            domain='.kingdoms.com'
        )

    def get_gameworld(self, gw_name, avatar_name=None):
        gameworld = Gameworld(client=self.client)
        if avatar_name:
            avatar_id = self._get_avatar_id(gw_name, avatar_name)
            gameworld.authenticate(gameworld_name=gw_name, avatar_id=avatar_id)
        else:
            gw_id = self._get_gw_id(gw_name)
            gameworld.authenticate(gameworld_name=gw_name, gameworld_id=gw_id)
        return gameworld

    def _get_gw_id(self, gameworld):
        r = self.cache.get({'names':['Collection:Avatar']})
        for avatar in r['cache'][0]['data']['cache']:
            if gameworld == avatar['data']['worldName'].lower():
                gameworld_id = avatar['data']['consumersId']
                return gameworld_id
        raise AvatarNotFound(f'Avatar on {gameworld} not found')

    def _get_avatar_id(self, gameworld, avatar_name):
        for x in ['Collection:Sitter:1', 'Collection:Sitter:4']:
            r = self.cache.get({'names':[x]})
            for avatar in r['cache'][0]['data']['cache']:
                if avatar['data']['avatarName'] == avatar_name and avatar['data']['worldName'].lower() == gameworld:
                    return avatar['data']['avatarIdentifier']
        raise AvatarNotFound(f'Avatar {avatar_name} on {gameworld} not found.')

    @property
    def session(self):
        encoded_session = self.client.get_cookie(
            name='gl5SessionKey',
            domain='lobby.kingdoms.com'
        )
        return json.loads(parse.unquote(encoded_session))['key']

    @property
    def lobby_id(self):
        return self.client.get_cookie(
            name='gl5PlayerId',
            domain='lobby.kingdoms.com'
        )

    @property
    def msid(self):
        return self.client.get_cookie(
            name='msid',
            domain='.kingdoms.com'
        )

    def post(self, controller, action, params={}):
        params = {
            'action': action,
            'controller': controller,
            'params': params,
            'session': self.session
        }
        r = self.client.post(url=Lobby.api_root, json=params)
        return r.json()


class Gameworld:
    def __init__(self, client):
        self.client = client
        self.gameConfig = dict() # Travian Config
        self.accountDetails = dict() # account details

        # Controllers
        self.player = player.Player(post_handler=self.post)
        self.farmList = farmList.FarmList(post_handler=self.post)
        self.logger = logger.Logger(post_handler=self.post)
        self.troops = troops.Troops(post_handler=self.post)
        self.village = village.Village(post_handler=self.post)
        self.cache = cache.Cache(post_handler=self.post)
        self.quest = quest.Quest(post_handler=self.post)
        self.error = error.Error(post_handler=self.post)
        self.auctions = auctions.Auctions(post_handler=self.post)
        self.hero = hero.Hero(post_handler=self.post)
        self.building = building.Building(post_handler=self.post)
        self.trade = trade.Trade(post_handler=self.post)
        self.ranking = ranking.Ranking(post_handler=self.post)
        self.kingdom = kingdom.Kingdom(post_handler=self.post)
        self.map = map.Map(post_handler=self.post)
        self.reports = reports.Reports(post_handler=self.post)
        self.society = society.Society(post_handler=self.post)
        self.premiumFeature = premiumFeature.PremiumFeature(post_handler=self.post)
        self.payment = payment.Payment(post_handler=self.post)
        self.kingdomTreaty = kingdomTreaty.KingdomTreaty(post_handler=self.post)
        self.login = login.Login(post_handler=self.post)

    def is_authenticated(self):
        try:
            self.troops.getMarkers()
        except:
            raise

    def authenticate(self, gameworld_name, gameworld_id=None, avatar_id=None):
        self.client.cookies.set(
            name='gameworld',
            value=gameworld_name,
            domain='www.example.com'
        )
        mellon_url = 'https://mellon-t5.traviangames.com'
        if gameworld_id:
            r = self.client.get(
                f'{mellon_url}/game-world/join/gameWorldId/{gameworld_id}?msid={self.msid}&msname=msid'
            )
        else:
            r = self.client.get(
                f'{mellon_url}/game-world/join-as-guest/avatarId/{avatar_id}?msid={self.msid}&msname=msid'
            )
        token = r.text[r.text.find('token=')+6: r.text.find('token=')+38]
        r = self.client.get(
            f'https://{gameworld_name.lower()}.kingdoms.com/api/login.php?token={token}&msid={self.msid}&msname=msid'
        )
        # add travian config
        self.gameConfig.update(
            json.loads(
                r.text[r.text.find('Travian.Config = {\"feature')+17:r.text.find('Travian.Config.worldRadius =')-1]
            )
        )
        self.update_account()

    def update_account(self):
        r = self.cache.get({'names':[f'Player:{self.player_id}']})
        self.accountDetails.update(
            r['cache'][0]['data']
        )

    @property
    def gameworld(self):
        return self.client.get_cookie(
            name='gameworld',
            domain='www.example.com'
        )

    @property
    def api_root(self):
        return 'https://%s.kingdoms.com/api/?' % self.gameworld

    @property
    def msid(self):
        return self.client.get_cookie(
            name='msid',
            domain='.kingdoms.com'
        )

    @property
    def decoded_session(self):
        encoded_session = self.client.get_cookie(
            name='t5SessionKey',
            domain=self.api_root[8:-6]
        )
        return json.loads(parse.unquote(encoded_session))

    @property
    def player_id(self):
        return int(self.decoded_session['id'])

    @property
    def session(self):
        return self.decoded_session['key']

    @property
    def tribe_id(self):
        return int(self.accountDetails['tribeId'])

    @property
    def kingdom_id(self):
        return int(self.accountDetails['kingdomId'])

    @property
    def plus_account(self):
        return int(self.accountDetails['plusAccountTime'])

    def post(self, controller, action, params={}):
        payload = {
            'action': action,
            'controller': controller,
            'params': params,
            'session': self.session
        }
        timestamp = int('{:.3f}'.format(time.time()).replace('.', ''))
        url = f'{self.api_root}c={controller}&a={action}&t{timestamp}'
        r = self.client.post(url=url, json=payload)
        if 'error' in r.json():
            raise NotAuthenticated()
        return r.json()
