from tkpy.database import BASE_DIR
from tkpy.database import CredentialDb
from tkpy.exception import DriverNotFound
from unittest.mock import patch, Mock
import unittest
import pickle


class TestCredentialDb(unittest.TestCase):

    @patch('tkpy.database.pickle')
    @patch('tkpy.database.sqlite3')
    @patch('tkpy.database.os')
    def testing_credential_db_that_already_exist(self, mock_os, mock_sqlite, mock_pickle):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            pickled_driver = f.read()

        g = pickle.loads(pickled_driver)

        mock_os.path = Mock()
        mock_os.path.join.return_value = '/temp/credential.db'
        mock_os.path.isfile.return_value = True

        mock_sqlite.connect().cursor().fetchone.return_value = pickled_driver

        db = CredentialDb('dummy@email.com', 'dummypassword', 'com93')
        db.get()
        mock_os.path.join.assert_called_with(BASE_DIR, 'credential.db')
        mock_os.path.isfile.assert_called_with('/temp/credential.db')
        mock_sqlite.connect.assert_called_with('/temp/credential.db')

        db.update(driver=g)
        mock_pickle.dumps.assert_called_with(g)
        mock_sqlite.connect.assert_called_with('/temp/credential.db')

        db.insert(driver=g)
        mock_pickle.dumps.assert_called_with(g)
        mock_sqlite.connect.assert_called_with('/temp/credential.db')

        mock_sqlite.connect().cursor().fetchone.return_value = None
        with self.assertRaises(DriverNotFound):
            db.get()

    @patch('tkpy.database.pickle')
    @patch('tkpy.database.sqlite3')
    @patch('tkpy.database.os')
    def testing_credential_db_that_not_exist(self, mock_os, mock_sqlite, mock_pickle):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            pickled_driver = f.read()

        g = pickle.loads(pickled_driver)

        mock_os.path = Mock()
        mock_os.path.join.return_value = '/temp/credential.db'
        mock_os.path.isfile.return_value = False

        db = CredentialDb('dummy@email.com', 'dummypassword', 'com93')
        mock_os.path.isfile.assert_called_with('/temp/credential.db')
        mock_sqlite.connect.assert_called_with('/temp/credential.db')

        db.get()
        mock_os.path.join.assert_called_with(BASE_DIR, 'credential.db')
        mock_os.path.isfile.assert_called_with('/temp/credential.db')
        mock_sqlite.connect.assert_called_with('/temp/credential.db')

        db.update(driver=g)
        mock_pickle.dumps.assert_called_with(g)
        mock_sqlite.connect.assert_called_with('/temp/credential.db')

        db.insert(driver=g)
        mock_pickle.dumps.assert_called_with(g)
        mock_sqlite.connect.assert_called_with('/temp/credential.db')

        mock_sqlite.connect().cursor().fetchone.return_value = None
        with self.assertRaises(DriverNotFound):
            db.get()


if __name__ == '__main__':
    unittest.main()
