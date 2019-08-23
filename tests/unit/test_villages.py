from tkpy.villages import Village
from tkpy.villages import Villages
from tkpy.exception import VillageNotFound
from tkpy.exception import WarehouseNotEnough
from tkpy.exception import QueueFull
from tkpy.exception import BuildingSlotFull
from tkpy.exception import BuildingAtMaxLevel
from tkpy.exception import FailedConstructBuilding
from tkpy.exception import NotAuthenticated
from tkpy.exception import TargetNotFound
import unittest
import requests_mock
import pickle
import json


class TestVillages(unittest.TestCase):

    def setUp(self):
        with open('tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            self.g = pickle.load(f)

        with open('tests/unit/fixtures/villages_raw.json', 'r') as f:
            self.villages_raw = json.load(f)

        self.url = 'https://com93.kingdoms.com/api/'

    def testing_villages(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json=self.villages_raw
            )
            v = Villages(self.g)
            v.pull()

        self.assertEqual(v['001'].name, '001')
        self.assertEqual(len(list(v.dorps)), 2)
        v_capital = v.get_capital_village()
        self.assertEqual(v_capital.name, '001')
        with self.assertRaises(VillageNotFound):
            v['villages not found']


class TestVillage(unittest.TestCase):

    def setUp(self):
        with open('tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            self.g = pickle.load(f)

        with open('./tests/unit/fixtures/village_raw.json', 'r') as f:
            self.village_raw = json.load(f)

        with open('./tests/unit/fixtures/village_units_raw.json', 'r') as f:
            self.village_units_raw = json.load(f)

        with open('./tests/unit/fixtures/construction_list_raw.json', 'r') as f:
            self.construction_list_raw = json.load(f)

        with open('./tests/unit/fixtures/send_troops_raw.json', 'r') as f:
            self.send_troops_raw = json.load(f)

        with open('./tests/unit/fixtures/raw_troops_movement.json', 'r') as f:
            self.troops_movement_raw = json.load(f)

        with open('./tests/unit/fixtures/cell_details.json', 'r') as f:
            self.cell_details = json.load(f)

        with open('./tests/unit/fixtures/cell_details2.json', 'r') as f:
            self.cell_details2 = json.load(f)

        with open('./tests/unit/fixtures/buildings_raw.json', 'r') as f:
            self.buildings_raw = json.load(f)

        with open('./tests/unit/fixtures/building_queue_raw.json', 'r') as f:
            self.building_queue_raw = json.load(f)

        self.village = Village(
            client=self.g,
            data=self.village_raw['cache'][0]['data']
        )

        self.url = 'https://com93.kingdoms.com/api/'

    def assertRaisesMessage(self, exc, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.assertFail()
        except Exception as e:
            self.assertTrue(e.__class__ == exc)
            self.assertEqual(e.msg, msg)

    def testing_village_attribute(self):
        v = Village(
            client=self.g,
            data=self.village_raw['cache'][0]['data']
        )
        self.assertEqual(v.name, '001')
        self.assertEqual(v.villageId, '536461288')
        self.assertEqual(v.coordinates, {'x': '-24', 'y': '-13'})
        self.assertTrue(v.isMainVillage)
        self.assertFalse(v.isTown)

    def testing_village_pull(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json=self.village_raw
            )
            self.village.pull()
        self.assertEqual(self.village.name, '001')
        self.assertEqual(self.village.villageId, '536461288')
        self.assertEqual(self.village.coordinates, {'x': '-24', 'y': '-13'})
        self.assertTrue(self.village.isMainVillage)
        self.assertFalse(self.village.isTown)

    def testing_village_units(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json=self.village_units_raw
            )
            r = self.village.units()
        self.assertEqual(r, {'1': '122', '2': '14', '4': '1', '11': '1'})

    def testing_village_troops_movement(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json=self.troops_movement_raw
            )
            r = self.village.troops_movement()
        self.assertEqual(r, [])

    def testing_village_attack_raised_target_not_found(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json=self.cell_details
            )
            with self.assertRaises(TargetNotFound):
                r = self.village.attack(0, 0)

    def testing_village_attack(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.cell_details2},
                    {'json': self.village_units_raw},
                    {'json': self.send_troops_raw},
                ]
            )
            r = self.village.attack(1, 1)
        self.assertEqual(r, self.send_troops_raw)

    def testing_village_raid(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.cell_details2},
                    {'json': self.village_units_raw},
                    {'json': self.send_troops_raw},
                ]
            )
            r = self.village.raid(1, 1)
        self.assertEqual(r, self.send_troops_raw)

    def testing_village_defend(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.cell_details2},
                    {'json': self.village_units_raw},
                    {'json': self.send_troops_raw},
                ]
            )
            r = self.village.defend(1, 1)
        self.assertEqual(r, self.send_troops_raw)

    def testing_village_spy(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.cell_details2},
                    {'json': self.village_units_raw},
                    {'json': self.send_troops_raw},
                ]
            )
            r = self.village.spy(1, 1, amount=1)
        self.assertEqual(r, self.send_troops_raw)

    def testing_village_siege_but_failed(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.cell_details2},
                    {'json': self.village_units_raw},
                    {'json': self.send_troops_raw},
                ]
            )
            # with self.assertRaises(SyntaxError):
                # r = self.village.siege(1, 1)
            self.assertRaisesMessage(
                SyntaxError,
                'Set units first',
                self.village.siege, 1, 1, None, None
            )

    def testing_village_send_farmlist(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json={'mock': 'mocked'}
            )
            r = self.village.send_farmlist([123])
        self.assertEqual(r, {'mock': 'mocked'})

    def testing_village_upgrade(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.village_raw},
                    {'json': self.buildings_raw},
                    {'json': self.building_queue_raw},
                    {'json': {'mock': 'mocked'}},
                ]
            )
            r = self.village.upgrade('main building')
        self.assertEqual(r, {'mock': 'mocked'})

    def testing_village_warehouse(self):
        self.assertEqual(self.village.warehouse.storage, {"1": 260.78677256557, "2": 200.1046366545, "3": 194.46890847656, "4": 180.21246008591})
        self.assertEqual(self.village.warehouse.production, {"1": 1290, "2": 990, "3": 960, "4": 890})
        self.assertEqual(self.village.warehouse.capacity, {"1": 22500, "2": 22500, "3": 22500, "4": 15000})
        self.assertEqual(self.village.warehouse.wood, '260.78677256557/22500 1290')
        self.assertEqual(self.village.warehouse.clay, '200.1046366545/22500 990')
        self.assertEqual(self.village.warehouse.iron, '194.46890847656/22500 960')
        self.assertEqual(self.village.warehouse.crop, '180.21246008591/15000 890')
        self.assertEqual(self.village.warehouse['1'], 260.78677256557)
        self.assertEqual(self.village.warehouse['wood'], 260.78677256557)
        with self.assertRaises(KeyError):
            self.village.warehouse['key error']




if __name__ == '__main__':
    unittest.run()
