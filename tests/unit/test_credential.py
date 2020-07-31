from tkpy.models.credential import Lobby
from tkpy.models.credential import Gameworld
from tkpy.models.credential import dict_parser
from tkpy.models.credential import query_maker
from unittest.mock import Mock, patch
import unittest


class TestingDictParser(unittest.TestCase):
    def testing_dict_parser(self):
        data = {"mock": "mocked", "mocked": "mock"}
        result = dict_parser(data)

        self.assertEqual(data, result)


class TestingQueryMaker(unittest.TestCase):
    def testing_query_maker(self):
        data = {"mock": "mocked", "mocked": "mock"}
        query = query_maker(data)

        self.assertEqual(query, "mock = ? AND mocked = ?")


class TestingLobby(unittest.TestCase):
    @patch("tkpy.models.credential.hashlib")
    @patch("tkpy.models.credential.binascii")
    def testing_lobby_hash_password(self, mock_binascii, mock_hashlib):
        mock_hashlib.sha256().hexdigest().encode.return_value = b"this has "
        mock_hashlib.pbkdf2_hmac.return_value = b"mocked pbkdf2"
        mock_binascii.hexlify.return_value = b"been mocked"
        string = Mock()
        string.encode.return_value = b"mocked string"
        p = Lobby.hash_password(string)
        self.assertEqual(p, "this has been mocked")

    @patch("tkpy.models.credential.hashlib")
    @patch("tkpy.models.credential.binascii")
    def testing_lobby_verify_password(self, mock_binascii, mock_hashlib):
        mock_binascii.hexlify().decode.return_value = "mocked"
        Lobby.verify_password(
            "50b2eeedfd4c1ad7c12665f4ca9c68a339d68c988a1e6b9e7b00ca2d64a1cbe697d3c61351e945a9d7532391aca2b07a7c2d56291248463f7d669ad8e45d57806148f7b05cc23f78674908ed56eaad3a4bd122875f2a15f0db1309052685b0a5",
            "moked",
        )

    @patch("tkpy.models.credential.get_connection")
    def testing_lobby_find_one(self, mock_get_connection):
        r = Lobby.find_one(id=1)

        mock_get_connection.return_value.__enter__.assert_called()

    @patch("tkpy.models.credential.get_connection")
    def testing_lobby_create(self, mock_get_connection):
        r = Lobby.create("email@testing.com", "testingpassword")

        mock_get_connection.return_value.__enter__.assert_called()


class TestingGameworld(unittest.TestCase):
    @patch("tkpy.models.credential.get_connection")
    def testing_gameworld_find_one(self, mock_get_connection):
        r = Gameworld.find_one(id=1)

        mock_get_connection.return_value.__enter__.assert_called()

    @patch("tkpy.models.credential.get_connection")
    def testing_gameworld_update(self, mock_get_connection):
        Gameworld.update({"driver": "mocked"}, {"id": 1})

        mock_get_connection.return_value.__enter__.assert_called()

    @patch("tkpy.models.credential.get_connection")
    def testing_gameworld_create(self, mock_get_connection):
        r = Gameworld.create("com99", "mocked", 2)

        mock_get_connection.return_value.__enter__.assert_called()
