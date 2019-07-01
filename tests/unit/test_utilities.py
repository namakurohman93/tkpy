from tkpy.utilities import credential
from tkpy.utilities import _login
from tkpy.utilities import login
from tkpy.utilities import send_troops
from tkpy.utilities import send_farmlist
from tkpy.utilities import instant_finish
from tkpy.utilities import upgrade_building
from tkpy.utilities import queue_building
from tkpy.exception import DriverNotFound, NotAuthenticated
from unittest.mock import patch, Mock
import unittest
import requests_mock
import pickle
import json
import sys


class TestCredential(unittest.TestCase):

    def testing_credential_without_avatar(self):
        args = ['script', 'dummy@email.com', 'dummypassword', 'com93']
        with patch.object(sys, 'argv', args):
            email, password, gameworld, avatar = credential()

            self.assertEqual(email, 'dummy@email.com')
            self.assertEqual(password, 'dummypassword')
            self.assertEqual(gameworld, 'com93')
            self.assertEqual(avatar, None)

    def testing_credential_with_avatar(self):
        args = ['script', 'dummy@email.com', 'dummypassword', 'com93', '--avatar', 'dummyavatar']
        with patch.object(sys, 'argv', args):
            email, password, gameworld, avatar = credential()

            self.assertEqual(email, 'dummy@email.com')
            self.assertEqual(password, 'dummypassword')
            self.assertEqual(gameworld, 'com93')
            self.assertEqual(avatar, 'dummyavatar')


class Test_Login(unittest.TestCase):

    def testing_login(self):
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

            g = _login('dummy@email.com', 'dummypassword', 'com93', None)
            self.assertEqual(g.session, '6a07238e83ccc69977ea')
            self.assertEqual(g.player_id, 123)
            self.assertEqual(g.gameworld, 'com93')
            self.assertEqual(g.api_root, 'https://com93.kingdoms.com/api/?')


class TestLogin(unittest.TestCase):

    @patch('tkpy.utilities.CredentialDb')
    def testing_login_that_found_the_driver(self, mock_db):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with open('./tests/unit/fixtures/step_15.json', 'r') as f:
            step_15 = json.load(f)

        mock_get = mock_db.return_value
        mock_get.get.return_value = g
        with requests_mock.mock() as m:
            m.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json={'mock': 'mocked'}
            )
            m.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json=step_15
            )
            gw = login('dummy@email.com', 'dummypassword', 'com93')
            mock_get.get.assert_called_once()
            self.assertEqual(gw.session, '6a07238e83ccc69977ea')
            self.assertEqual(gw.player_id, 123)
            self.assertEqual(gw.gameworld, 'com93')
            self.assertEqual(gw.api_root, 'https://com93.kingdoms.com/api/?')

    @patch('tkpy.utilities.CredentialDb')
    def testing_login_that_have_expired_session(self, mock_db):
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

        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with requests_mock.mock() as m:
            m.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json={'error': 'mocked'}
            )
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
            instance = mock_db.return_value
            mock_driver = Mock()
            mock_driver.is_authenticated.side_effect = NotAuthenticated()
            instance.get.return_value = mock_driver
            gw = login('dummy@email.com', 'dummypassword', 'com93')
            instance.update.assert_called()
            self.assertEqual(gw.session, '6a07238e83ccc69977ea')
            self.assertEqual(gw.player_id, 123)
            self.assertEqual(gw.gameworld, 'com93')
            self.assertEqual(gw.api_root, 'https://com93.kingdoms.com/api/?')

    @patch('tkpy.utilities.CredentialDb')
    def testing_login_that_not_found_the_driver(self, mock_db):
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
            instance = mock_db.return_value
            instance.get.side_effect = DriverNotFound()
            gw = login('dummy@email.com', 'dummypassword', 'com93')
            instance.insert.assert_called()
            self.assertEqual(gw.session, '6a07238e83ccc69977ea')
            self.assertEqual(gw.player_id, 123)
            self.assertEqual(gw.gameworld, 'com93')
            self.assertEqual(gw.api_root, 'https://com93.kingdoms.com/api/?')


class TestSendTroops(unittest.TestCase):

    def test_send_troops(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json={'mock': 'mocked'}
            )
            r = send_troops(
                driver=g,
                destVillageId=123123123,
                movementType=123,
                redeployHero=False,
                spyMission='resources',
                units={'1':1, '2':2},
                villageId=123123
            )
            self.assertEqual(r, {'mock': 'mocked'})


class TestSendFarmlist(unittest.TestCase):

    def test_send_farmlist(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json={'mock': 'mocked'}
            )
            r = send_farmlist(
                driver=g,
                listIds=123123,
                villageId=123123
            )
            self.assertEqual(r, {'mock': 'mocked'})


class TestInstantFinish(unittest.TestCase):

    def test_instant_finish(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json={'mock': 'mocked'}
            )
            r = instant_finish(
                driver=g,
                queueType=1,
                villageId=1
            )
            self.assertEqual(r, {'mock': 'mocked'})


class TestUpgradeBuilding(unittest.TestCase):

    def test_upgrade_building(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json={'mock': 'mocked'}
            )
            r = upgrade_building(
                driver=g,
                buildingType=12,
                locationId=11,
                villageId=123123
            )
            self.assertEqual(r, {'mock': 'mocked'})


class TestQueueBuilding(unittest.TestCase):

    def test_queue_building(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json={'mock': 'mocked'}
            )
            r = queue_building(
                driver=g,
                buildingType=1,
                locationId=1,
                villageId=1,
                reserveResources=True
            )
            self.assertEqual(r, {'mock': 'mocked'})


if __name__ == '__main__':
    unittest.main()
