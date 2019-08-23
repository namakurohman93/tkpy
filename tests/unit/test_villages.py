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

        with open('./tests/unit/fixtures/construction_list_raw.json', 'r') as f:
            self.construction_list_raw = json.load(f)

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
            self.assertEqual(e.__class__, exc)
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

    def testing_village_attack_raise_there_is_no_troops_on_village_syntax_error(self):
        self.village_units_raw['cache'][0]['data']['cache'][0]['data']['units'] = {}
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.cell_details2},
                    {'json': self.village_units_raw},
                ]
            )
            self.assertRaisesMessage(
                SyntaxError,
                'There is no troops on 001 village',
                self.village.attack, 1, 1, None, None
            )

    def testing_village_attack_use_all_troops(self):
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
            r = self.village.attack(1, 1, units={'1':-1, '2':-1, '3':-1, '4':-1, '5':-1, '6':-1, '7':-1, '8':-1, '9':-1, '10':-1, '11':-1})
        self.assertEqual(r, self.send_troops_raw)

    def testing_village_attack_raise_not_enough_troops_syntax_error(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.cell_details2},
                    {'json': self.village_units_raw},
                ]
            )
            self.assertRaisesMessage(
                SyntaxError,
                'Not enough troops 1',
                self.village.attack, 1, 1, None, {'1': 10000000}
            )

    def testing_village_attack_raise_send_at_least_1_troop_syntax_error(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.cell_details2},
                    {'json': self.village_units_raw},
                ]
            )
            self.assertRaisesMessage(
                SyntaxError,
                'Send at least 1 troops',
                self.village.attack, 1, 1, None, {'1':0, '2':0}
            )

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

    def testing_village_spy_raise_choose_mission_between_resources_or_defence_syntax_error(self):
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.cell_details2},
                    {'json': self.village_units_raw},
                ]
            )
            self.assertRaisesMessage(
                SyntaxError,
                "choose mission between 'resources' or 'defence'",
                self.village.spy, 1, 1, None, 1, 'error'
            )

    def testing_village_siege_raise_set_unit_first_syntax_error(self):
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
            self.assertRaisesMessage(
                SyntaxError,
                'Set units first',
                self.village.siege, 1, 1, None, None
            )

    def testing_village_siege_raise_need_at_least_1000_troops_syntax_error(self):
        self.village_units_raw['cache'][0]['data']['cache'][0]['data']['units']['7'] = 1
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.cell_details2},
                    {'json': self.village_units_raw},
                ]
            )
            self.assertRaisesMessage(
                SyntaxError,
                'Need at least 1000 troops',
                self.village.siege, 1, 1, None, {'1': 1, '7': 1}
            )

    def testing_village_siege_raise_need_at_least_1_ram_for_siege_syntax_error(self):
        self.village_units_raw['cache'][0]['data']['cache'][0]['data']['units']['1'] = 1000
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.cell_details2},
                    {'json': self.village_units_raw},
                ]
            )
            self.assertRaisesMessage(
                SyntaxError,
                'Need at least 1 ram for siege',
                self.village.siege, 1, 1, None, {'1': 1000}
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
        # this upgrade building goes to queues cause there is not enough
        # resources but queue slot has free slot
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

    def testing_village_upgrade_again(self):
        # this upgrade building goes to upgrade slot cause now it
        # have enough resources
        self.buildings_raw['cache'][0]['data']['cache'][0]['data']['upgradeCosts'] = {'1': 0, '2': 0, '3': 0, '4': 0}
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

    def testing_village_upgrade_again_but_building_go_to_queue_slot(self):
        # this upgrade building goes to upgrade slot cause now it
        # have enough resources, but it didn't go to upgrade slot
        # cause upgrade slot currently being used by other building,
        # so this building goes to queue slot
        self.buildings_raw['cache'][0]['data']['cache'][0]['data']['upgradeCosts'] = {'1': 0, '2': 0, '3': 0, '4': 0}
        self.building_queue_raw['cache'][0]['data']['freeSlots']['1'] = 0
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

    def testing_village_upgrade_with_building_at_max_level(self):
        self.buildings_raw['cache'][0]['data']['cache'][0]['data']['isMaxLvl'] = True
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.village_raw},
                    {'json': self.buildings_raw},
                    {'json': self.building_queue_raw},
                ]
            )
            with self.assertRaises(BuildingAtMaxLevel):
                self.village.upgrade('main building')

    def testing_village_ugprade_building_but_raise_queue_full_exception(self):
        self.building_queue_raw['cache'][0]['data']['freeSlots']['4'] = 0
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.village_raw},
                    {'json': self.buildings_raw},
                    {'json': self.building_queue_raw},
                ]
            )
            with self.assertRaises(QueueFull):
                self.village.upgrade('main building')

    def testing_village_upgrade_that_didnt_exists(self):
        # it mean :meth:`Village._construct` will be called
        # and this call will add building to queue slot
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.village_raw},
                    {'json': self.buildings_raw},
                    {'json': self.building_queue_raw},
                    {'json': self.construction_list_raw},
                    {'json': {'mock': 'mocked'}},
                ]
            )
            r = self.village.upgrade('smithy')
        self.assertEqual(r, {'mock': 'mocked'})

    def testing_village_upgrade_that_didnt_exists_again(self):
        # it mean :meth:`Village._construct` will be called
        # this time it will add building to upgrade slot cause now it
        # have enough resources
        self.construction_list_raw['response']['buildings']['buildable'][0]['upgradeCosts'] = {'1': 0, '2': 0, '3': 0, '4': 0}
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.village_raw},
                    {'json': self.buildings_raw},
                    {'json': self.building_queue_raw},
                    {'json': self.construction_list_raw},
                    {'json': {'mock': 'mocked'}},
                ]
            )
            r = self.village.upgrade('smithy')
        self.assertEqual(r, {'mock': 'mocked'})

    def testing_village_upgrade_that_didnt_exists_but_raise_warehouse_not_enough_exception(self):
        # it mean :meth:`Village._construct` will be called
        self.construction_list_raw['response']['buildings']['buildable'][0]['upgradeCosts']['1'] = 9999999
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.village_raw},
                    {'json': self.buildings_raw},
                    {'json': self.building_queue_raw},
                    {'json': self.construction_list_raw},
                ]
            )
            with self.assertRaises(WarehouseNotEnough):
                self.village.upgrade('smithy')

    def testing_village_upgrade_that_didnt_exists_but_raise_failed_construct_building_exception(self):
        # it mean :meth:`Village._construct` will be called
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.village_raw},
                    {'json': self.buildings_raw},
                    {'json': self.building_queue_raw},
                    {'json': self.construction_list_raw},
                ]
            )
            with self.assertRaises(FailedConstructBuilding):
                self.village.upgrade('trade office')

    def testing_village_upgrade_that_didnt_exists_but_raise_building_slot_full_exception(self):
        # it mean :meth:`Village._construct` will be called
        for x in self.buildings_raw['cache'][0]['data']['cache']:
            x['data']['buildingType'] = '1'
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.village_raw},
                    {'json': self.buildings_raw},
                    {'json': self.building_queue_raw},
                    {'json': self.construction_list_raw},
                ]
            )
            with self.assertRaises(BuildingSlotFull):
                self.village.upgrade('smithy')

    def testing_village_upgrade_raises_warehouse_not_enough_exception(self):
        self.buildings_raw['cache'][0]['data']['cache'][0]['data']['upgradeCosts']['1'] = 9999999
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                [
                    {'json': self.village_raw},
                    {'json': self.buildings_raw},
                    {'json': self.building_queue_raw},
                ]
            )
            with self.assertRaises(WarehouseNotEnough):
                self.village.upgrade('main building')

    def testing_village_upgrade_tribe_roman_building_type_resources(self):
        self.g.accountDetails['tribeId'] = 1
        for x in self.buildings_raw['cache'][0]['data']['cache']:
            if x['data']['buildingType'] == '1':
                x['data']['upgradeCosts'] = {'1': 0, '2': 0, '3': 0, '4': 0}
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
            r = self.village.upgrade('wood')
        self.assertEqual(r, {'mock': 'mocked'})

    def testing_village_attack_with_different_tribe(self):
        self.g.accountDetails['tribeId'] = 3
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

    def testing_village_spy_with_different_tribe(self):
        self.village_units_raw['cache'][0]['data']['cache'][0]['data']['units']['3'] = 1
        self.g.accountDetails['tribeId'] = 3
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
