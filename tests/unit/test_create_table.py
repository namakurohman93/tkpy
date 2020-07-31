from tkpy.models.config import create_table
from unittest.mock import Mock
import unittest


class TestingCreateTable(unittest.TestCase):
    def testing_create_table(self):
        mocking = Mock()

        create_table(mocking)

        mocking.executescript.assert_called()
