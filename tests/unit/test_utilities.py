#  from tkpy.utilities import _login
#  from tkpy.utilities import login
#  from tkpy.utilities import credential
#  from tkpy.utilities import hash_password
#  from tkpy.utilities import verify_password
#  from tkpy.utilities import retrieve_data
#  from tkpy.utilities import commit_query
#  from tkpy.utilities import get_user_id
#  from tkpy.utilities import add_user
#  from tkpy.utilities import get_driver_id
#  from tkpy.utilities import insert_driver
#  from tkpy.utilities import update_driver
#  from tkpy.utilities import get_driver
#  from tkpy.exception import DriverNotFound, NotAuthenticated
#  from unittest.mock import patch, Mock
#  import unittest
#  import requests_mock
#  import pickle
#  import json
#  import sys


#  class TestCredential(unittest.TestCase):

    #  def testing_credential_without_avatar(self):
        #  args = ['script', 'dummy@email.com', 'dummypassword', 'com93']
        #  with patch.object(sys, 'argv', args):
            #  email, password, gameworld, avatar = credential()

            #  self.assertEqual(email, 'dummy@email.com')
            #  self.assertEqual(password, 'dummypassword')
            #  self.assertEqual(gameworld, 'com93')
            #  self.assertEqual(avatar, None)

    #  def testing_credential_with_avatar(self):
        #  args = ['script', 'dummy@email.com', 'dummypassword', 'com93', '--avatar', 'dummyavatar']
        #  with patch.object(sys, 'argv', args):
            #  email, password, gameworld, avatar = credential()

            #  self.assertEqual(email, 'dummy@email.com')
            #  self.assertEqual(password, 'dummypassword')
            #  self.assertEqual(gameworld, 'com93')
            #  self.assertEqual(avatar, 'dummyavatar')


#  class TestHashPassword(unittest.TestCase):

    #  @patch('tkpy.utilities.hashlib')
    #  @patch('tkpy.utilities.binascii')
    #  def test_hash_password(self, mock_binascii, mock_hashlib):
        #  mock_hashlib.sha256().hexdigest().encode.return_value = b'this has '
        #  mock_hashlib.pbkdf2_hmac.return_value = b'mocked pbkdf2'
        #  mock_binascii.hexlify.return_value = b'been mocked'
        #  string = Mock()
        #  string.encode.return_value = b'mocked string'
        #  p = hash_password(string)
        #  self.assertEqual(p, 'this has been mocked')


#  class TestVerifyPassword(unittest.TestCase):

    #  @patch('tkpy.utilities.hashlib')
    #  @patch('tkpy.utilities.binascii')
    #  def test_verify_password(self, mock_binascii, mock_hashlib):
        #  mock_binascii.hexlify().decode.return_value = 'mocked'
        #  verify_password('50b2eeedfd4c1ad7c12665f4ca9c68a339d68c988a1e6b9e7b00ca2d64a1cbe697d3c61351e945a9d7532391aca2b07a7c2d56291248463f7d669ad8e45d57806148f7b05cc23f78674908ed56eaad3a4bd122875f2a15f0db1309052685b0a5', 'moked')


#  class TestRetrieveData(unittest.TestCase):

    #  @patch('tkpy.utilities.get_db')
    #  def test_retrieve_data(self, mock_get_db):
        #  mock_get_db.return_value.__enter__.return_value.execute().fetchone.return_value = 'mocked'
        #  r = retrieve_data('mocking', 'mock')
        #  self.assertEqual(r, 'mocked')


#  class TestCommitQuery(unittest.TestCase):

    #  @patch('tkpy.utilities.get_db')
    #  def test_commit_query(self, mock_get_db):
        #  mock_commit = Mock()
        #  mock_get_db.return_value.__enter__.return_value.commit = mock_commit
        #  commit_query('mock', 'mocking')
        #  mock_commit.assert_called_once()


#  class TestGetUserId(unittest.TestCase):

    #  def setUp(self):
        #  self.cred = ('your@email.com', 'your password')

    #  @patch('tkpy.utilities.retrieve_data')
    #  @patch('tkpy.utilities.verify_password')
    #  def test_get_user_id(self, mock_verify, mock_retrieve):
        #  mock_retrieve.return_value = None
        #  u = get_user_id(*self.cred)
        #  self.assertEqual(u, None)
        #  mock_retrieve.return_value = {'password': 'mocked'}
        #  mock_verify.return_value = False
        #  with self.assertRaises(NotAuthenticated):
            #  u = get_user_id(*self.cred)
        #  mock_retrieve.return_value = {'password': 'mocked', 'id': 'mocked'}
        #  mock_verify.return_value = True
        #  u = get_user_id(*self.cred)
        #  self.assertEqual(u, 'mocked')


#  class TestAddUser(unittest.TestCase):

    #  @patch('tkpy.utilities.uuid')
    #  @patch('tkpy.utilities.commit_query')
    #  def test_add_user(self, mock_commit, mock_uuid):
        #  mock_uuid.uuid4().hex = 'mocked'
        #  uid = add_user('your@email.com', 'your password')
        #  mock_commit.assert_called_once()
        #  self.assertEqual(uid, 'mocked')


#  class TestGetDriverId(unittest.TestCase):

    #  @patch('tkpy.utilities.retrieve_data')
    #  def test_get_driver_id(self, mock_retrieve):
        #  mock_retrieve.return_value = None
        #  with self.assertRaises(DriverNotFound):
            #  driver = get_driver_id('mock', 'mock', 'mock')

        #  mock_retrieve.return_value = {'id': 'mocked'}
        #  driver = get_driver_id('mock', 'mock', 'mock')
        #  self.assertEqual(driver, 'mocked')


#  class TestInsertDriver(unittest.TestCase):

    #  @patch('tkpy.utilities.commit_query')
    #  def test_insert_driver(self, mock_commit):
        #  insert_driver('mock', 'mock', 'mock', 'mock')
        #  mock_commit.assert_called_once()


#  class TestUpdateDriver(unittest.TestCase):

    #  @patch('tkpy.utilities.commit_query')
    #  def test_update_driver(self, mock_commit):
        #  update_driver('mock', 'mock')
        #  mock_commit.assert_called_once()


#  class TestGetDriver(unittest.TestCase):

    #  @patch('tkpy.utilities.retrieve_data')
    #  @patch('tkpy.utilities.pickle')
    #  def test_get_driver(self, mock_pickle, mock_retrieve):
        #  mock_pickle.loads.return_value = 'mocked'
        #  d = get_driver('mock')
        #  self.assertEqual(d, 'mocked')
        #  mock_retrieve.assert_called_with('SELECT driver FROM gameworld WHERE id = ?', ('mock',))
        #  mock_retrieve.assert_called_once()
        #  mock_pickle.loads.assert_called_once()


#  class TestLogin(unittest.TestCase):

    #  def testing_login(self):
        #  with open('./tests/unit/fixtures/step_1.txt', 'r') as f:
            #  step_1 = f.read()

        #  with open('./tests/unit/fixtures/step_4.txt', 'r') as f:
            #  step_4 = f.read()

        #  with open('./tests/unit/fixtures/step_7.txt', 'r') as f:
            #  step_7 = f.read()

        #  with open('./tests/unit/fixtures/cookies.json', 'r') as f:
            #  c = json.load(f)

        #  jar = requests_mock.CookieJar()

        #  for x in ('gl5PlayerId', 'gl5SessionKey'):
            #  jar.set(
                #  x,
                #  c.get(x, None),
                #  domain='lobby.kingdoms.com',
                #  path='/'
            #  )

        #  with open('./tests/unit/fixtures/step_8.json', 'r') as f:
            #  step_8 = json.load(f)

        #  with open('./tests/unit/fixtures/step_10.txt', 'r') as f:
            #  step_10 = f.read()

        #  with open('./tests/unit/fixtures/step_13.txt', 'r') as f:
            #  step_13 = f.read()

        #  with open('./tests/unit/fixtures/step_15.json', 'r') as f:
            #  step_15 = json.load(f)

        #  jar2 = requests_mock.CookieJar()

        #  for x in ('t5SessionKey', 't5mu'):
            #  jar2.set(
                #  x,
                #  c.get(x, None),
                #  domain=f'{c.get("gameworld")}.kingdoms.com',
                #  path='/'
            #  )

        #  with requests_mock.mock() as m:
            #  m.register_uri(
                #  'GET',
                #  'https://mellon-t5.traviangames.com/authentication/login',
                #  text=step_1
            #  )
            #  m.register_uri(
                #  'POST',
                #  'https://mellon-t5.traviangames.com/authentication/login/ajax/form-validate?msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                #  text=step_4
            #  )
            #  m.register_uri(
                #  'GET',
                #  'https://lobby.kingdoms.com/api/login.php?token=5b717b2096697410478b2c0d77cfa8ad&msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                #  text=step_7,
                #  cookies=jar
            #  )
            #  m.register_uri(
                #  'POST',
                #  'https://lobby.kingdoms.com/api/index.php',
                #  json=step_8
            #  )
            #  m.register_uri(
                #  'GET',
                #  'https://mellon-t5.traviangames.com/game-world/join/gameWorldId/111?msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                #  text=step_10
            #  )
            #  m.register_uri(
                #  'GET',
                #  'https://com93.kingdoms.com/api/login.php?token=db3dad78c114051bfa01da3a452cea23&msid=hef39l99m6b9ae5gj42mf7udf4&msname=msid',
                #  text=step_13,
                #  cookies=jar2
            #  )
            #  m.register_uri(
                #  'POST',
                #  'https://com93.kingdoms.com/api/',
                #  json=step_15
            #  )

            #  g = login('dummy@email.com', 'dummypassword', 'com93', None)
            #  self.assertEqual(g.session, '6a07238e83ccc69977ea')
            #  self.assertEqual(g.player_id, 123)
            #  self.assertEqual(g.gameworld, 'com93')
            #  self.assertEqual(g.api_root, 'https://com93.kingdoms.com/api/?')


#  class Test_Login(unittest.TestCase):

    #  @patch('tkpy.utilities.get_user_id')
    #  @patch('tkpy.utilities.get_driver_id')
    #  @patch('tkpy.utilities.get_driver')
    #  def test_login_1(self, mock_get_driver, mock_get_driver_id, mock_get_user_id):
        #  mock_get_user_id.return_value = 'mocked user id'
        #  mock_get_driver_id.return_value = 'mocked driver id'
        #  mock_driver = Mock()
        #  mock_get_driver.return_value = mock_driver
        #  d = _login('mock email', 'mock password', 'mock gw')
        #  mock_get_user_id.assert_called_with('mock email', 'mock password')
        #  mock_get_driver_id.assert_called_with('mocked user id', 'mock gw', None)
        #  mock_get_driver.assert_called_with('mocked driver id')
        #  mock_driver.is_authenticated.assert_called_once()
        #  mock_driver.update_account.assert_called_once()

    #  @patch('tkpy.utilities.get_user_id')
    #  @patch('tkpy.utilities.insert_driver')
    #  @patch('tkpy.utilities.add_user')
    #  @patch('tkpy.utilities.get_driver_id')
    #  @patch('tkpy.utilities.login')
    #  def test_login_2(self, mock_login, mock_get_driver_id, mock_add_user, mock_insert_driver, mock_get_user_id):
        #  mock_add_user.return_value = 'mocked user id'
        #  mock_get_user_id.return_value = None
        #  mock_get_driver_id.side_effect = DriverNotFound
        #  mocked_driver = Mock()
        #  mock_login.return_value = mocked_driver
        #  d = _login('mock email', 'mock password', 'mock gw', 'mock avatar')
        #  mock_add_user.assert_called_with('mock email', 'mock password')
        #  mock_get_driver_id.assert_called_with('mocked user id', 'mock gw', 'mock avatar')
        #  mock_login.assert_called_with('mock email', 'mock password', 'mock gw', 'mock avatar')
        #  mock_insert_driver.assert_called_with('mocked user id', mocked_driver, 'mock gw', 'mock avatar')

    #  @patch('tkpy.utilities.get_user_id')
    #  @patch('tkpy.utilities.get_driver_id')
    #  @patch('tkpy.utilities.get_driver')
    #  @patch('tkpy.utilities.login')
    #  @patch('tkpy.utilities.update_driver')
    #  def test_login_3(self, mock_update_driver, mock_login, mock_get_driver, mock_get_driver_id, mock_get_user_id):
        #  mock_get_user_id.return_value = 'mocked user id'
        #  mock_get_driver_id.return_value = 'mocked driver id'
        #  mocked_driver = Mock()
        #  mocked_driver.is_authenticated.side_effect = NotAuthenticated
        #  mock_get_driver.return_value = mocked_driver
        #  mock_login.return_value = 'mocked driver'
        #  d = _login('mock email', 'mock password', 'mock gw', 'mock avatar')
        #  self.assertEqual(d, 'mocked driver')
        #  mock_get_user_id.assert_called_with('mock email', 'mock password')
        #  mock_get_driver_id.assert_called_with('mocked user id', 'mock gw', 'mock avatar')
        #  mock_get_driver.assert_called_with('mocked driver id')
        #  mock_login.assert_called_with('mock email', 'mock password', 'mock gw', 'mock avatar')
        #  mock_update_driver.assert_called_with('mocked driver id', 'mocked driver')


#  if __name__ == '__main__':
    #  unittest.main()
