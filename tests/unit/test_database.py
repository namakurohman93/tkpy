from unittest.mock import Mock, patch
from tkpy.database import get_db
import unittest


class Test(unittest.TestCase):

    @patch('tkpy.database.sqlite3')
    @patch('tkpy.database.get_db')
    def test_get_db(self, mock_get_db, mock_sqlite):
        mock_sqlite.connect().execute.return_value = 'mocked'
        mock_get_db.__enter__.return_value = mock_sqlite

        with get_db() as db:
            foo = db.execute('random things')

        self.assertEqual(foo, 'mocked')
        mock_sqlite.connect().execute.assert_called()


if __name__ == '__main__':
    unittest.main()
