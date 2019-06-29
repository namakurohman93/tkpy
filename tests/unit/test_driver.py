from tkpy.driver import Lobby
from tkpy.driver import HttpClient
from tkpy.driver import Gameworld
from tkpy.exception import NotAuthenticated, AvatarNotFound
import json
import unittest
import requests_mock


class TestHttpClient(unittest.TestCase):

    def testing_httpclient_without_cookies(self):
        jar = requests_mock.CookieJar()
        jar.set('mock', 'mocked')

        with requests_mock.mock() as m:
            m.register_uri(
                'GET',
                'https://www.kingdoms.com/get',
                text='get mocked',
                cookies=jar
            )
            m.register_uri(
                'POST',
                'https://www.kingdoms.com/post',
                text='post mocked',
                cookies=jar
            )

            client = HttpClient()

            r = client.get('https://www.kingdoms.com/get', timeout=10)
            self.assertEqual(r.text, 'get mocked')
            self.assertEqual(r.url, 'https://www.kingdoms.com/get')
            self.assertEqual(r.cookies, {'mock': 'mocked'})
            self.assertEqual(client.get_cookie('mock'), 'mocked')

            r = client.post('https://www.kingdoms.com/post')
            self.assertEqual(r.text, 'post mocked')
            self.assertEqual(r.url, 'https://www.kingdoms.com/post')
            self.assertEqual(r.cookies, {'mock': 'mocked'})
            self.assertEqual(client.get_cookie('mock'), 'mocked')

    def testing_httpclient_with_cookies(self):
        with open('./tests/unit/fixtures/cookies.json', 'r') as f:
            c = json.load(f)

        client = HttpClient(cookies=c)
        self.assertEqual(client.get_cookie('msid'), c.get('msid'))
        self.assertEqual(client.get_cookie('gl5SessionKey'), c.get('gl5SessionKey'))
        self.assertEqual(client.get_cookie('gl5PlayerId'), c.get('gl5PlayerId'))
        self.assertEqual(client.get_cookie('gameworld'), c.get('gameworld'))
        self.assertEqual(client.get_cookie('t5SessionKey'), c.get('t5SessionKey'))
        self.assertEqual(client.get_cookie('t5mu'), c.get('t5mu'))


class TestLobby(unittest.TestCase):

    def testing_lobby(self):
        with open('./tests/unit/fixtures/step_1.txt', 'r') as f:
            step_1 = f.read()

        with open('./tests/unit/fixtures/step_4.txt', 'r') as f:
            step_4 = f.read()

        with open('./tests/unit/fixtures/step_7.txt', 'r') as f:
            step_7 = f.read()

        with open('./tests/unit/fixtures/cookies.json', 'r') as f:
            c = json.load(f)

        jar = requests_mock.CookieJar()

        for x in ('gl5PlayerId', 'gl5SessionKey'):
            jar.set(
                x,
                c.get(x, None),
                domain='lobby.kingdoms.com',
                path='/'
            )

        with requests_mock.mock() as m:
            m.register_uri(
                'GET',
                'https://mellon-t5.traviangames.com/authentication/login',
                text=step_1
            )
            m.register_uri(
                'POST',
                'https://mellon-t5.traviangames.com/authentication/login/ajax/form-validate?msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_4
            )
            m.register_uri(
                'GET',
                'https://lobby.kingdoms.com/api/login.php?token=5b717b2096697410478b2c0d77cfa8ad&msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_7,
                cookies=jar
            )

            l = Lobby()
            l.authenticate('dummy@email.com', 'dummypassword')

        self.assertEqual(l.msid, 'hef39l99m6b9ae5gj42mf7udf4')
        self.assertEqual(l.lobby_id, '123123')
        self.assertEqual(l.session, 'a79f27f5799dbc13ca95')

    def testing_lobby_not_authenticate(self):
        with open('./tests/unit/fixtures/step_1.txt', 'r') as f:
            step_1 = f.read()

        with open('./tests/unit/fixtures/step_4.txt', 'r') as f:
            step_4 = f.read()

        with open('./tests/unit/fixtures/step_7.txt', 'r') as f:
            step_7 = f.read()

        with open('./tests/unit/fixtures/cookies.json', 'r') as f:
            c = json.load(f)

        jar = requests_mock.CookieJar()

        for x in ('gl5PlayerId', 'gl5SessionKey'):
            jar.set(
                x,
                c.get(x, None),
                domain='lobby.kingdoms.com',
                path='/'
            )

        with requests_mock.mock() as m:
            m.register_uri(
                'GET',
                'https://mellon-t5.traviangames.com/authentication/login',
                text=step_1
            )
            m.register_uri(
                'POST',
                'https://mellon-t5.traviangames.com/authentication/login/ajax/form-validate?msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_4
            )
            m.register_uri(
                'GET',
                'https://lobby.kingdoms.com/api/login.php?token=5b717b2096697410478b2c0d77cfa8ad&msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_7,
                cookies=jar
            )

            l = Lobby()
            l.authenticate('dummy@email.com', 'dummypassword')

        with requests_mock.mock() as m:
            mock = {'error': []}

            m.register_uri(
                'POST',
                'https://lobby.kingdoms.com/api/index.php',
                json=mock
            )

            with self.assertRaises(NotAuthenticated):
                l.is_authenticated()

    def testing_lobby_controllers(self):
        with open('./tests/unit/fixtures/step_1.txt', 'r') as f:
            step_1 = f.read()

        with open('./tests/unit/fixtures/step_4.txt', 'r') as f:
            step_4 = f.read()

        with open('./tests/unit/fixtures/step_7.txt', 'r') as f:
            step_7 = f.read()

        with open('./tests/unit/fixtures/cookies.json', 'r') as f:
            c = json.load(f)

        jar = requests_mock.CookieJar()

        for x in ('gl5PlayerId', 'gl5SessionKey'):
            jar.set(
                x,
                c.get(x, None),
                domain='lobby.kingdoms.com',
                path='/'
            )

        with requests_mock.mock() as m:
            m.register_uri(
                'GET',
                'https://mellon-t5.traviangames.com/authentication/login',
                text=step_1
            )
            m.register_uri(
                'POST',
                'https://mellon-t5.traviangames.com/authentication/login/ajax/form-validate?msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_4
            )
            m.register_uri(
                'GET',
                'https://lobby.kingdoms.com/api/login.php?token=5b717b2096697410478b2c0d77cfa8ad&msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_7,
                cookies=jar
            )

            l = Lobby()
            l.authenticate('dummy@email.com', 'dummypassword')

        mock = {'mock': 'mocked'}

        with requests_mock.mock() as m:
            m.register_uri(
                'POST',
                'https://lobby.kingdoms.com/api/index.php',
                json=mock
            )

            r = l.achievements.update()
            self.assertEqual(r, mock)

            r = l.cache.get({'names':['mocking']})
            self.assertEqual(r, mock)

            r = l.dual.add({'avatarIdentifier': 0, 'consumersId': 'mock', 'avatarName': 'mock', 'email': 'mock'})
            self.assertEqual(r, mock)

            r = l.gameworld.getPossibleNewGameworlds()
            self.assertEqual(r, mock)

            r = l.login.logout()
            self.assertEqual(r, mock)

            r = l.notification.markAsRead({'id': 'mock'})
            self.assertEqual(r, mock)

            r = l.player.getAll({'deviceDimension': 'mock'})
            self.assertEqual(r, mock)

            r = l.player.abortDeletion({'avatarIdentifier': 'mock'})
            self.assertEqual(r, mock)

            r = l.sitter.add({'avatarIdentifier': 123, 'consumersId': 'mock', 'avatarName': 'mock', 'email': 'mock'})
            self.assertEqual(r, mock)

            r = l.sitter.setPermissions({'avatarIdentifier': 123, 'sitterAccountIdentifier': 123, 'permissions': {'1': False, '2': False, '3': False, '4': False}})
            self.assertEqual(r, mock)

            r = l.sitter.remove({'avatarIdentifier': 123, 'sitterAccountIdentifier': 123})
            self.assertEqual(r, mock)


class TestGameworld(unittest.TestCase):

    def test_gameworld_without_avatar(self):
        with open('./tests/unit/fixtures/step_1.txt', 'r') as f:
            step_1 = f.read()

        with open('./tests/unit/fixtures/step_4.txt', 'r') as f:
            step_4 = f.read()

        with open('./tests/unit/fixtures/step_7.txt', 'r') as f:
            step_7 = f.read()

        with open('./tests/unit/fixtures/cookies.json', 'r') as f:
            c = json.load(f)

        jar = requests_mock.CookieJar()

        for x in ('gl5PlayerId', 'gl5SessionKey'):
            jar.set(
                x,
                c.get(x, None),
                domain='lobby.kingdoms.com',
                path='/'
            )

        with requests_mock.mock() as m:
            m.register_uri(
                'GET',
                'https://mellon-t5.traviangames.com/authentication/login',
                text=step_1
            )
            m.register_uri(
                'POST',
                'https://mellon-t5.traviangames.com/authentication/login/ajax/form-validate?msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_4
            )
            m.register_uri(
                'GET',
                'https://lobby.kingdoms.com/api/login.php?token=5b717b2096697410478b2c0d77cfa8ad&msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_7,
                cookies=jar
            )

            l = Lobby()
            l.authenticate('dummy@email.com', 'dummypassword')

        with open('./tests/unit/fixtures/step_8.json', 'r') as f:
            step_8 = json.load(f)

        with open('./tests/unit/fixtures/step_10.txt', 'r') as f:
            step_10 = f.read()

        with open('./tests/unit/fixtures/step_13.txt', 'r') as f:
            step_13 = f.read()

        with open('./tests/unit/fixtures/step_15.json', 'r') as f:
            step_15 = json.load(f)

        jar2 = requests_mock.CookieJar()

        for x in ('t5SessionKey', 't5mu'):
            jar2.set(
                x,
                c.get(x, None),
                domain=f'{c.get("gameworld")}.kingdoms.com',
                path='/'
            )

        with requests_mock.mock() as m:
            m.register_uri(
                'POST',
                'https://lobby.kingdoms.com/api/index.php',
                json=step_8
            )
            m.register_uri(
                'GET',
                'https://mellon-t5.traviangames.com/game-world/join/gameWorldId/111?msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_10
            )
            m.register_uri(
                'GET',
                'https://com93.kingdoms.com/api/login.php?token=db3dad78c114051bfa01da3a452cea23&msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_13,
                cookies=jar2
            )
            m.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json=step_15
            )

            with self.assertRaises(AvatarNotFound):
                g = l.get_gameworld('com233333')

            g = l.get_gameworld('com93')
            self.assertEqual(g.session, '6a07238e83ccc69977ea')
            self.assertEqual(g.player_id, 123)
            self.assertEqual(g.gameworld, 'com93')
            self.assertEqual(g.api_root, 'https://com93.kingdoms.com/api/?')

    def test_gameworld_with_avatar(self):
        with open('./tests/unit/fixtures/step_1.txt', 'r') as f:
            step_1 = f.read()

        with open('./tests/unit/fixtures/step_4.txt', 'r') as f:
            step_4 = f.read()

        with open('./tests/unit/fixtures/step_7.txt', 'r') as f:
            step_7 = f.read()

        with open('./tests/unit/fixtures/cookies.json', 'r') as f:
            c = json.load(f)

        jar = requests_mock.CookieJar()

        for x in ('gl5PlayerId', 'gl5SessionKey'):
            jar.set(
                x,
                c.get(x, None),
                domain='lobby.kingdoms.com',
                path='/'
            )

        with requests_mock.mock() as m:
            m.register_uri(
                'GET',
                'https://mellon-t5.traviangames.com/authentication/login',
                text=step_1
            )
            m.register_uri(
                'POST',
                'https://mellon-t5.traviangames.com/authentication/login/ajax/form-validate?msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_4
            )
            m.register_uri(
                'GET',
                'https://lobby.kingdoms.com/api/login.php?token=5b717b2096697410478b2c0d77cfa8ad&msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_7,
                cookies=jar
            )

            l = Lobby()
            l.authenticate('dummy@email.com', 'dummypassword')

        with open('./tests/unit/fixtures/step_8.json', 'r') as f:
            step_8 = json.load(f)

        with open('./tests/unit/fixtures/step_10.txt', 'r') as f:
            step_10 = f.read()

        with open('./tests/unit/fixtures/step_13.txt', 'r') as f:
            step_13 = f.read()

        with open('./tests/unit/fixtures/step_15.json', 'r') as f:
            step_15 = json.load(f)

        jar2 = requests_mock.CookieJar()

        for x in ('t5SessionKey', 't5mu'):
            jar2.set(
                x,
                c.get(x, None),
                domain=f'{c.get("gameworld")}.kingdoms.com',
                path='/'
            )

        with requests_mock.mock() as m:
            m.register_uri(
                'POST',
                'https://lobby.kingdoms.com/api/index.php',
                json=step_8
            )
            m.register_uri(
                'GET',
                'https://mellon-t5.traviangames.com/game-world/join-as-guest/avatarId/123456?msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_10
            )
            m.register_uri(
                'GET',
                'https://com93.kingdoms.com/api/login.php?token=db3dad78c114051bfa01da3a452cea23&msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                text=step_13,
                cookies=jar2
            )
            m.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json=step_15
            )

            with self.assertRaises(AvatarNotFound):
                g = l.get_gameworld('com233333', 'asdfasdf')

            g = l.get_gameworld('com93', 'Mock 1')
            self.assertEqual(g.session, '6a07238e83ccc69977ea')
            self.assertEqual(g.player_id, 123)
            self.assertEqual(g.gameworld, 'com93')
            self.assertEqual(g.api_root, 'https://com93.kingdoms.com/api/?')
            self.assertEqual(g.tribe_id, 2)
            self.assertEqual(g.kingdom_id, 1)
            self.assertEqual(g.plus_account, -1)

            with requests_mock.mock() as m:
                mock = {'error': []}

                m.register_uri(
                    'POST',
                    'https://com93.kingdoms.com/api/?',
                    json=mock
                )

                with self.assertRaises(NotAuthenticated):
                    g.is_authenticated()


if __name__ == '__main__':
    unittest.main()
