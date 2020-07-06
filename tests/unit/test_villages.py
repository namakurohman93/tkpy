from tkpy.villages import Villages
from tkpy.exception import VillageNotFound
from tkpy.exception import WarehouseNotEnough
from tkpy.exception import QueueFull
from tkpy.exception import BuildingSlotFull
from tkpy.exception import BuildingAtMaxLevel
from tkpy.exception import FailedConstructBuilding
from tkpy.exception import TargetNotFound
import unittest
import requests_mock
import pickle
import json


class TestVillages(unittest.TestCase):

    def testing_villages(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with open('./tests/unit/fixtures/villages_raw.json', 'r') as f:
            villages_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json=villages_raw
            )
            v = Villages(g)
            v.pull()
        self.assertEqual(v['001'].name, '001')
        self.assertEqual(len(list(x for x in v)), 2)
        self.assertEqual(len(list(v._raw_data)), 2)
        v_capital = v.get_capital_village()
        self.assertEqual(v_capital.name, '001')
        with self.assertRaises(VillageNotFound):
            v['villages not found']

    def testing_village(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with open('./tests/unit/fixtures/villages_raw.json', 'r') as f:
            villages_raw = json.load(f)

        with open('./tests/unit/fixtures/village_raw.json', 'r') as f:
            village_raw = json.load(f)

        with open('./tests/unit/fixtures/village_units_raw.json', 'r') as f:
            village_units_raw = json.load(f)

        with open('./tests/unit/fixtures/construction_list_raw.json', 'r') as f:
            construction_list_raw = json.load(f)

        with open('./tests/unit/fixtures/send_troops_raw.json', 'r') as f:
            send_troops_raw = json.load(f)

        with open('./tests/unit/fixtures/send_troops_raw_failed.json', 'r') as f:
            send_troops_raw_failed = json.load(f)

        with open('./tests/unit/fixtures/raw_troops_movement.json', 'r') as f:
            troops_movement_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json=villages_raw
            )
            v = Villages(g)
            v.pull()
        v1 = v['001']
        self.assertEqual(v1.id, 536461288)
        self.assertEqual(v1.name, '001')
        self.assertEqual(v1['name'], '001')
        self.assertEqual(v1.coordinate, (-24, -13))
        self.assertTrue(v1.is_main_village)
        with self.assertRaises(KeyError):
            v1['key error']

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json=village_raw
            )
            v['001'].pull()
        self.assertEqual(v1.id, 536461288)
        self.assertEqual(v1.name, '001')
        self.assertEqual(v1.coordinate, (-24, -13))
        self.assertTrue(v1.is_main_village)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json=troops_movement_raw
            )
            r = v['001'].troops_movement()
            self.assertEqual(r, [])

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json=village_units_raw
            )
            r = v1.units()
            self.assertEqual(r, {'1': '122', '2': '14', '4': '1', '11': '1'})

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            r = v1.attack(1, 1)
            self.assertEqual(r, send_troops_raw)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            r = v1._send_troops(x=1, y=1, destVillageId=None, movementType=3, redeployHero=False, spyMission='resources', units=None)
            self.assertEqual(r, send_troops_raw)

        with requests_mock.mock() as mock:
            village_units_raw['cache'][0]['data']['cache'][0]['data']['units'] = {'1': '122', '2': '14', '3': '10', '4': '1', '11': '1'}
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            r = v1.spy(1, 1, amount=1)
            self.assertEqual(r, send_troops_raw)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            r = v1.attack(1, 1, units={'1': -1})
            self.assertEqual(r, send_troops_raw)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            with self.assertRaises(SyntaxError):
                v1.attack(1, 1, units={'1': 123})

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            with self.assertRaises(SyntaxError):
                v1.attack(1, 1, units={'1': 0})

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            r = v1.raid(1, 1)
            self.assertEqual(r, send_troops_raw)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            r = v1.defend(1, 1)
            self.assertEqual(r, send_troops_raw)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            r = v1.spy(1, 1, amount=1)
            self.assertEqual(r, send_troops_raw)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            with self.assertRaises(SyntaxError):
                v1.spy(1, 1, amount=1, mission='error')

        with requests_mock.mock() as mock:
            village_units_raw['cache'][0]['data']['cache'][0]['data']['units'] = {'1': '1000', '7': '1'}
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            r = v1.siege(1, 1, units={'1':1000, '7':1})
            self.assertEqual(r, send_troops_raw)

        with requests_mock.mock() as mock:
            village_units_raw['cache'][0]['data']['cache'][0]['data']['units'] = {'1': '1000', '7': '1'}
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            with self.assertRaises(SyntaxError):
                v1.siege(1, 1, units={'1':1, '7':1})

        with requests_mock.mock() as mock:
            village_units_raw['cache'][0]['data']['cache'][0]['data']['units'] = {'1': '1000', '7': '1'}
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            with self.assertRaises(SyntaxError):
                v1.siege(1, 1)

        with requests_mock.mock() as mock:
            village_units_raw['cache'][0]['data']['cache'][0]['data']['units'] = {'1': '1000', '7': '1'}
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            with self.assertRaises(SyntaxError):
                v1.siege(1, 1, units={'1':1000})

        with requests_mock.mock() as mock:
            village_units_raw['cache'][0]['data']['cache'][0]['data']['units'] = {'1': '0', '7': '0'}
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw}
                ]
            )
            with self.assertRaises(SyntaxError):
                v1.attack(1, 1)

        with requests_mock.mock() as mock:
            village_units_raw['cache'][0]['data']['cache'][0]['data']['units'] = {'1': '111', '7': '111'}
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json': village_units_raw},
                    {'json': send_troops_raw_failed},
                ]
            )
            with self.assertRaises(TargetNotFound):
                v1.attack(1, 1)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json={'mock': 'mocked'}
            )
            r = v1.send_farmlist([123])
            self.assertEqual(r, {'mock': 'mocked'})

        with open('./tests/unit/fixtures/buildings_raw.json', 'r') as f:
            buildings_raw = json.load(f)

        with open('./tests/unit/fixtures/building_queue_raw.json', 'r') as f:
            building_queue_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':{'mock': 'mocked'}}
                ]
            )
            r = v1.upgrade('main building')
            self.assertEqual(r, {'mock': 'mocked'})

        buildings_raw['cache'][0]['data']['cache'][0]['data']['upgradeCosts']['1'] = 9999999
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':{'mock': 'mocked'}}
                ]
            )
            with self.assertRaises(WarehouseNotEnough):
                v1.upgrade('main building')

        buildings_raw['cache'][0]['data']['cache'][0]['data']['upgradeCosts']['1'] = 1210
        building_queue_raw['cache'][0]['data']['freeSlots']['4'] = 0
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':{'mock': 'mocked'}}
                ]
            )
            with self.assertRaises(QueueFull):
                v1.upgrade('main building')

        buildings_raw['cache'][0]['data']['cache'][0]['data']['upgradeCosts'] = {'1': 0, '2': 0, '3': 0, '4': 0}
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':{'mock': 'mocked'}}
                ]
            )
            r = v1.upgrade('main building')
            self.assertEqual(r, {'mock': 'mocked'})

        building_queue_raw['cache'][0]['data']['freeSlots']['1'] = 0
        building_queue_raw['cache'][0]['data']['freeSlots']['4'] = 1
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':{'mock': 'mocked'}}
                ]
            )
            r = v1.upgrade('main building')
            self.assertEqual(r, {'mock': 'mocked'})

        building_queue_raw['cache'][0]['data']['freeSlots']['4'] = 0
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':{'mock': 'mocked'}}
                ]
            )
            with self.assertRaises(QueueFull):
                v1.upgrade('main building')

        building_queue_raw['cache'][0]['data']['freeSlots']['1'] = 1
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':{'mock': 'mocked'}}
                ]
            )
            r = v1.upgrade('main building')
            self.assertEqual(r, {'mock': 'mocked'})

        building_queue_raw['cache'][0]['data']['freeSlots']['1'] = 0
        building_queue_raw['cache'][0]['data']['freeSlots']['4'] = 1
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':{'mock': 'mocked'}}
                ]
            )
            r = v1.upgrade('main building')
            self.assertEqual(r, {'mock': 'mocked'})

        building_queue_raw['cache'][0]['data']['freeSlots']['4'] = 0
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':{'mock': 'mocked'}}
                ]
            )
            with self.assertRaises(QueueFull):
                v1.upgrade('main building')

        buildings_raw['cache'][0]['data']['cache'][0]['data']['isMaxLvl'] = True
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':construction_list_raw}
                ]
            )
            with self.assertRaises(BuildingAtMaxLevel):
                v1.upgrade('main building')

        building_queue_raw['cache'][0]['data']['freeSlots']['4'] = 1
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':construction_list_raw}
                ]
            )
            v1.upgrade('smithy')

        for x in buildings_raw['cache'][0]['data']['cache']:
            if x['data']['buildingType'] == '1':
                x['data']['upgradeCosts'] = {'1': 0, '2': 0, '3': 0, '4': 0}
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':{'mock': 'mocked'}}
                ]
            )
            r = v1.upgrade('wood')
            self.assertEqual(r, {'mock': 'mocked'})

        building_queue_raw['cache'][0]['data']['freeSlots']['2'] = 0
        building_queue_raw['cache'][0]['data']['freeSlots']['4'] = 1
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':{'mock': 'mocked'}}
                ]
            )
            r = v1.upgrade('wood')
            self.assertEqual(r, {'mock': 'mocked'})

        building_queue_raw['cache'][0]['data']['freeSlots']['4'] = 0
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                [
                    {'json':village_raw},
                    {'json':buildings_raw},
                    {'json':building_queue_raw},
                    {'json':{'mock': 'mocked'}}
                ]
            )
            with self.assertRaises(QueueFull):
                v1.upgrade('wood')

    def test_village_construct(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with open('./tests/unit/fixtures/villages_raw.json', 'r') as f:
            villages_raw = json.load(f)

        with open('./tests/unit/fixtures/village_raw.json', 'r') as f:
            village_raw = json.load(f)

        with open('./tests/unit/fixtures/buildings_raw.json', 'r') as f:
            buildings_raw = json.load(f)

        with open('./tests/unit/fixtures/building_queue_raw.json', 'r') as f:
            building_queue_raw = json.load(f)

        with open('./tests/unit/fixtures/construction_list_raw.json', 'r') as f:
            construction_list_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json=villages_raw
            )
            v = Villages(g)
            v.pull()
            v1 = v['001']

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=cache&a=get',
                [
                    {'json': village_raw},
                    {'json': buildings_raw},
                    {'json': building_queue_raw}
                ]
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=building&a=getBuildingList',
                json=construction_list_raw
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=building&a=useMasterBuilder',
                json={'mock': 'mocked'}
            )
            v1.pull()
            v1.buildings.pull()
            v1.buildingQueue.pull()
            r = v1._construct('smithy')
            self.assertEqual(r, {'mock': 'mocked'})

        building_queue_raw['cache'][0]['data']['freeSlots']['4'] = 0
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=cache&a=get',
                [
                    {'json': village_raw},
                    {'json': buildings_raw},
                    {'json': building_queue_raw}
                ]
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=building&a=getBuildingList',
                json=construction_list_raw
            )
            v1.pull()
            v1.buildings.pull()
            v1.buildingQueue.pull()
            with self.assertRaises(QueueFull):
                v1._construct('smithy')

        building_queue_raw['cache'][0]['data']['freeSlots']['4'] = 1
        construction_list_raw['response']['buildings']['buildable'][0]['upgradeCosts']['1'] = 9999999999
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=cache&a=get',
                [
                    {'json': village_raw},
                    {'json': buildings_raw},
                    {'json': building_queue_raw}
                ]
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=building&a=getBuildingList',
                json=construction_list_raw
            )
            v1.pull()
            v1.buildings.pull()
            v1.buildingQueue.pull()
            with self.assertRaises(WarehouseNotEnough):
                v1._construct('smithy')

        construction_list_raw['response']['buildings']['buildable'][0]['upgradeCosts'] = {'1': 0, '2': 0, '3': 0, '4': 0}
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=cache&a=get',
                [
                    {'json': village_raw},
                    {'json': buildings_raw},
                    {'json': building_queue_raw}
                ]
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=building&a=getBuildingList',
                json=construction_list_raw
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=building&a=upgrade',
                json={'mock': 'mocked'}
            )
            v1.pull()
            v1.buildings.pull()
            v1.buildingQueue.pull()
            r = v1._construct('smithy')
            self.assertEqual(r, {'mock': 'mocked'})

        building_queue_raw['cache'][0]['data']['freeSlots']['1'] = 0
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=cache&a=get',
                [
                    {'json': village_raw},
                    {'json': buildings_raw},
                    {'json': building_queue_raw}
                ]
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=building&a=getBuildingList',
                json=construction_list_raw
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=building&a=useMasterBuilder',
                json={'mock': 'mocked'}
            )
            v1.pull()
            v1.buildings.pull()
            v1.buildingQueue.pull()
            r = v1._construct('smithy')
            self.assertEqual(r, {'mock': 'mocked'})

        building_queue_raw['cache'][0]['data']['freeSlots']['4'] = 0
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=cache&a=get',
                [
                    {'json': village_raw},
                    {'json': buildings_raw},
                    {'json': building_queue_raw}
                ]
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=building&a=getBuildingList',
                json=construction_list_raw
            )
            v1.pull()
            v1.buildings.pull()
            v1.buildingQueue.pull()
            with self.assertRaises(QueueFull):
                v1._construct('smithy')

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=cache&a=get',
                [
                    {'json': village_raw},
                    {'json': buildings_raw},
                    {'json': building_queue_raw}
                ]
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=building&a=getBuildingList',
                json=construction_list_raw
            )
            v1.pull()
            v1.buildings.pull()
            v1.buildingQueue.pull()
            with self.assertRaises(FailedConstructBuilding):
                v1._construct('stable')

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=cache&a=get',
                [
                    {'json': village_raw},
                    {'json': buildings_raw},
                    {'json': building_queue_raw}
                ]
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=building&a=getBuildingList',
                json=construction_list_raw
            )
            v1.pull()
            v1.buildings.pull()
            v1.buildingQueue.pull()
            with self.assertRaises(BuildingAtMaxLevel):
                v1._construct('main building')

        for x in buildings_raw['cache'][0]['data']['cache']:
            x['data']['buildingType'] = '1'
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=cache&a=get',
                [
                    {'json': village_raw},
                    {'json': buildings_raw},
                    {'json': building_queue_raw}
                ]
            )
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/?c=building&a=getBuildingList',
                json=construction_list_raw
            )
            v1.pull()
            v1.buildings.pull()
            v1.buildingQueue.pull()
            with self.assertRaises(BuildingSlotFull):
                v1._construct('smithy')

    def test_village_warehouse(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with open('./tests/unit/fixtures/villages_raw.json', 'r') as f:
            villages_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json=villages_raw
            )
            v = Villages(g)
            v.pull()
            v1 = v['001']
            self.assertEqual(v1.warehouse.storage, {'1': 929.07843923224, '2': 712.9796366545, '3': 691.80224180989, '4': 641.28190453036})
            self.assertEqual(v1.warehouse.production, {'1': 1290, '2': 990, '3': 960, '4': 890})
            self.assertEqual(v1.warehouse.capacity, {'1': 22500, '2': 22500, '3': 22500, '4': 15000})
            self.assertEqual(v1.warehouse.wood, '929.07843923224/22500 1290')
            self.assertEqual(v1.warehouse.clay, '712.9796366545/22500 990')
            self.assertEqual(v1.warehouse.iron, '691.80224180989/22500 960')
            self.assertEqual(v1.warehouse.crop, '641.28190453036/15000 890')
            self.assertEqual(v1.warehouse['1'], 929.07843923224)
            self.assertEqual(v1.warehouse['wood'], 929.07843923224)
            with self.assertRaises(KeyError):
                v1.warehouse['key error']

if __name__ == '__main__':
    unittest.main()
