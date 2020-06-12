from tkpy.notepads import Notepad
import requests_mock
import unittest
import pickle
import json


class TestNotepad(unittest.TestCase):

    def testing_notepad(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json={'cache':[{'data':{'cache':['mocked']}}]}
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json={'mock': 'mocked'}
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json={'cache':[{'data':{'cache':[{'data':{'id':1}}]}}]}
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json={'cache':[{'data':{'cache':[{'data':{'id':1}}]}}]}
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json={'cache':[{'data':{'cache':[{'data':{'id':1}}]}}]}
            )
            n = Notepad(g)
            n.message('Mocked')

    def testing_notepad_2(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':{'cache':[{'data':{'cache':[]}}]}},
                    {'json':{'cache':[]}},
                    {'json':{'cache':[{'data':{'cache':[{'data':{'id':1}}]}}]}},
                    {'json':{'cache':[]}},
                    {'json':{'cache':[]}},
                    {'json':{'cache':[]}}
                ]
            )
            n = Notepad(g)
            n.message('Mocked')


if __name__ == '__main__':
    unittest.main()
