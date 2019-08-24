from unittest.mock import Mock, patch
from tkpy.database import get_db
from tkpy.database import init_db
import unittest


class Test(unittest.TestCase):

    def setUp(self):
        with open('./tkpy/schema.sql', 'r') as f:
            self.schema = f.read()

    @patch('tkpy.database.sqlite3')
    @patch('tkpy.database.get_db')
    def test_get_db(self, mock_get_db, mock_sqlite):
        mock_sqlite.connect().execute.return_value = 'mocked'
        mock_get_db.__enter__.return_value = mock_sqlite

        with get_db() as db:
            foo = db.execute('random things')

        self.assertEqual(foo, 'mocked')
        mock_sqlite.connect().execute.assert_called()

    @patch('tkpy.database.get_db')
    def test_init_db(self, mock_get_db):
        init_db()
        mock_get_db.return_value.__enter__.return_value.executescript.assert_called_with(
            self.schema
        )


if __name__ == '__main__':
    unittest.main()
