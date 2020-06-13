from tkpy.farmlist import Farmlist
from tkpy.exception import FarmListNotFound
import unittest
import requests_mock
import pickle
import json


class TestFarmlist(unittest.TestCase):

    def setUp(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            self.g = pickle.load(f)

        with open('./tests/unit/fixtures/farmlist_raw.json', 'r') as f:
            self.farmlist_raw = json.load(f)

        self.url = 'https://com93.kingdoms.com/api/'

    def testing_farmlist(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json=self.farmlist_raw
            )
            fl = Farmlist(self.g)
            fl.pull()
        self.assertEqual(len(list(fl.list)), 3)
        self.assertEqual(fl['01'].listName, '01')
        with self.assertRaises(FarmListNotFound):
            fl['key not found']

    def testing_farmlist_create_farmlist(self):
        self.farmlist_raw['cache'][0]['data']['cache'].append(self.farmlist_raw['cache'][0]['data']['cache'][2])
        self.farmlist_raw['cache'][0]['data']['cache'][3]['data']['listName'] = 'test'
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': {'mock': 'mocked'}},
                    {'json': self.farmlist_raw}
                ]
            )
            fl = Farmlist(self.g)
            fl.create_farmlist('test')
            self.assertEqual(fl['test'].listName, 'test')


class TestFarmlistEntry(unittest.TestCase):

    def setUp(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            self.g = pickle.load(f)

        with open('./tests/unit/fixtures/farmlist_raw.json', 'r') as f:
            self.farmlist_raw = json.load(f)

        with open('./tests/unit/fixtures/farmlist_entry_raw.json', 'r') as f:
            self.farmlist_entry_raw = json.load(f)

        with open('./tests/unit/fixtures/farmlist_entry_pull_raw.json', 'r') as f:
            self.farmlist_entry_pull_raw = json.load(f)

        self.url = 'https://com93.kingdoms.com/api/'

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json=self.farmlist_raw
            )
            self.farmlist = Farmlist(self.g)
            self.farmlist.pull()

    def testing_farmlist_entry_attribute(self):
        fle = self.farmlist['01']
        self.assertEqual(fle.listName, '01')
        self.assertEqual(fle.listId, 1398)
        self.assertEqual(len(fle.villageIds), 10)
        self.assertEqual(len(fle.entryIds), 10)
        self.assertEqual(fle.maxEntriesCount, 100)
        self.assertFalse(fle.isDefault)
        self.assertEqual(fle.lastSent, 1561872785)
        self.assertEqual(fle.lastChanged, 1561849070)
        self.assertEqual(fle.units, {'1': '0', '2': '0', '3': '0', '4': '0', '5': '10', '6': '0'})
        self.assertEqual(fle.orderNr, 2)

    def testing_farmlist_entry_send(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json={'mock': 'mocked'}
            )
            r = self.farmlist['01'].send(123)
            self.assertEqual(r, {'mock': 'mocked'})

    def testing_farmlist_entry_add(self):
        fle = self.farmlist['01']
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json=self.farmlist_entry_raw
            )
            fle.add(535150570)
        self.assertEqual(len(fle.villageIds), 11)
        self.assertEqual(len(fle.entryIds), 11)
        self.assertTrue('535150570' in fle.villageIds)

    def testing_farmlist_entry_toggle(self):
        fle = self.farmlist['01']
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json=self.farmlist_entry_raw
            )
            fle.toggle(535150570)
        self.assertEqual(len(fle.villageIds), 11)
        self.assertEqual(len(fle.entryIds), 11)
        self.assertTrue('535150570' in fle.villageIds)

    def testing_farmlist_entry_pull(self):
        fle = self.farmlist['01']
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json=self.farmlist_entry_pull_raw
            )
            fle.pull()
        self.assertEqual(len(list(fle.farmlistEntry)), 11)


class TestEntryId(unittest.TestCase):

    def setUp(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            self.g = pickle.load(f)

        with open('./tests/unit/fixtures/farmlist_raw.json', 'r') as f:
            self.farmlist_raw = json.load(f)

        with open('./tests/unit/fixtures/farmlist_entry_pull_raw.json', 'r') as f:
            self.farmlist_entry_pull_raw = json.load(f)

        self.url = 'https://com93.kingdoms.com/api/'

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json=self.farmlist_raw
            )
            self.farmlist = Farmlist(self.g)
            self.farmlist.pull()

        fle = self.farmlist['01']
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json=self.farmlist_entry_pull_raw
            )
            fle.pull()
        fl_list = list(fle.farmlistEntry)
        self.entry_id = fl_list[0]

    def testing_entry_id_attribute(self):
        self.assertEqual(self.entry_id.entryId, 6350)
        self.assertEqual(self.entry_id.villageId, 535150570)
        self.assertEqual(self.entry_id.villageName, 'kolobelix 1')
        self.assertEqual(self.entry_id.units, {'1': '0', '2': '0', '3': '0', '4': '0', '5': '0', '6': '0'})
        self.assertEqual(self.entry_id.coords, {'x': '-22', 'y': '-53'})
        self.assertEqual(self.entry_id.targetOwnerId, 1302)
        self.assertEqual(self.entry_id.belongsToKing, 203)
        self.assertEqual(self.entry_id.population, 300)
        self.assertEqual(self.entry_id.lastReport, None)
        self.assertFalse(self.entry_id.isOasis)
        # class properties
        self.assertEqual(self.entry_id.notification_type, '0')
        self.assertEqual(self.entry_id.raided_sum, 0)
        self.assertEqual(self.entry_id.capacity, 0)

    def testing_entry_id_copy(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json={'mock': 'mocked'}
            )
            self.entry_id.copy(123)

    def testing_entry_id_delete(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json={'mock': 'mocked'}
            )
            self.entry_id.delete()


if __name__ == '__main__':
    unittest.main()
