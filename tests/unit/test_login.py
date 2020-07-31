from tkpy.login import authenticate
import unittest
from unittest.mock import patch
from unittest.mock import Mock


class TestAuthenticate(unittest.TestCase):
    @patch("tkpy.login.LobbyModel")
    @patch("tkpy.login.GameworldModel")
    @patch("tkpy.login.pickle")
    def testing_authenticate_with_success_result(
        self, mock_pickle, mock_gameworld, mock_lobby
    ):
        mock_lobby.find_one().execute.return_value = "mocked"
        mock_lobby.verify_password().execute.return_value = True
        mock_gameworld.find_one().execute.return_value = "mocked"
        mock_driver = Mock()
        mock_driver.is_authenticated().execute.return_value = True
        mock_pickle.loads().execute.return_value = mock_driver

        driver = authenticate("testing@email.com", "testingpassword", "com99")

        mock_lobby.find_one.assert_called()
        mock_lobby.find_one.assert_called_with(email="testing@email.com")
        mock_lobby.verify_password.assert_called()
        mock_gameworld.find_one.assert_called()
        mock_driver.is_authenticated.assert_called()
