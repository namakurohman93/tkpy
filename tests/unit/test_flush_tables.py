from tkpy.models import flush_tables
from unittest.mock import patch
import unittest


class TestingFlushTables(unittest.TestCase):
    @patch("tkpy.models.get_connection")
    def testing_flush_tables(self, mock_get_connection):
        flush_tables()
