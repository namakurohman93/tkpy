from tkpy.buildings import Buildings
from tkpy.buildings import BuildingQueue
from tkpy.buildings import ConstructionList
import unittest
import requests_mock
import pickle
import json


class TestBuildings(unittest.TestCase):

    def testing_buildings(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with open('./tests/unit/fixtures/buildings_raw.json', 'r') as f:
            buildings_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json=buildings_raw
            )
            b = Buildings(g, 536461288)
            b.pull()
        self.assertEqual(len(b['crop']), 6)
        self.assertEqual(len(b.freeSlots), 8)
        self.assertEqual(len(list(b.raw)), 40)
        self.assertEqual(b['crop'][0].id, '4')
        self.assertEqual(b['crop'][0]['buildingType'], '4')
        self.assertEqual(b['crop'][0].location, '2')
        self.assertEqual(b['crop'][0].lvl, 6)
        self.assertFalse(b['crop'][0].isMaxLvl)
        self.assertEqual(b['crop'][0].upgradeCost, {'1': 1625, '2': 1950, '3': 1845, '4': 0})
        with self.assertRaises(KeyError):
            b['crop'][0]['KeyError']

        with requests_mock.mock() as mock:
                mock.register_uri(
                    'POST',
                    'https://com93.kingdoms.com/api/',
                    json={'mock': 'mocked'}
                )
                r = b['crop'][0].upgrade()
                self.assertEqual(r, {'mock': 'mocked'})
                r = b['crop'][0].queues(reserveResources=False)
                self.assertEqual(r, {'mock': 'mocked'})

    def testing_building_queue(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with open('./tests/unit/fixtures/building_queue_raw.json', 'r') as f:
            building_queue_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json=building_queue_raw
            )
            bq = BuildingQueue(g, 536461288)
            bq.pull()
        self.assertEqual(bq.tribe_id, 2)
        self.assertEqual(bq.freeSlots, {'1':1, '2':1, '4':1})
        self.assertEqual(bq.queues, {'1':[], '2':[], '4':[], '5':[]})

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json={'mock': 'mocked'}
            )
            r = bq.finishNow(2)
            self.assertEqual(r, {'mock': 'mocked'})

    def testing_construction_list(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with open('./tests/unit/fixtures/construction_list_raw.json', 'r') as f:
            construction_list_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json=construction_list_raw
            )
            c = ConstructionList(g, 536461288, '39')
            c.pull()
        self.assertEqual(len(c.buildable), 4)
        self.assertEqual(len(c.notBuildable), 8)
        self.assertEqual(c['cranny'], {})
        self.assertFalse(c['iron foundry']['buildable'])
        self.assertTrue(c['smithy']['buildable'])
        with self.assertRaises(KeyError):
            c['KeyError']


if __name__ == '__main__':
    unittest.main()
