from tkpy.models.connection import get_connection
from unittest.mock import patch, Mock
import unittest


class TestingGetConnection(unittest.TestCase):
    @patch("tkpy.models.connection.sqlite3")
    @patch("tkpy.models.connection.create_table")
    def testing_get_connection(self, mock_create_table, mock_sqlite):
        with get_connection() as conn:
            foo = conn.execute("random things")

        mock_sqlite.connect().execute.assert_called()
