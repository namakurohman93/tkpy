from tkpy.villages import Villages
from tkpy.exception import QueueFull
from tkpy.exception import VillageNotFound
from tkpy.exception import BuildingSlotFull
from tkpy.exception import BuildingAtMaxLevel
from tkpy.exception import WarehouseNotEnough
from tkpy.exception import FailedConstructBuilding
from tkpy.enums.tribe import Tribe
from tkpy.enums.building import BuildingType
import unittest
import requests_mock
import pickle
import json


class TestVillages(unittest.TestCase):
    def testing_villages(self):
        g = None
        v = None
        villages_raw = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/villages_raw.json", "r") as f:
            villages_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=villages_raw
            )
            v = Villages(g)
            v.pull()

        self.assertEqual(v["001"].name, "001")
        self.assertEqual(len(list(x for x in v)), 2)
        self.assertEqual(len(list(v.keys())), 2)
        self.assertEqual(len(list(v.items())), 2)
        self.assertEqual(len(list(v.values())), 2)
        with self.assertRaises(VillageNotFound):
            v["village not found"]

        cv = v.get_capital_village()
        self.assertEqual(cv.name, "001")


class TestVillage(unittest.TestCase):
    def testing_property_village(self):
        g = None
        v = None
        villages_raw = {}
        village_raw = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/villages_raw.json", "r") as f:
            villages_raw = json.load(f)

        with open("./tests/unit/fixtures/village_raw.json", "r") as f:
            village_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=villages_raw
            )
            v = Villages(g)
            v.pull()

        v1 = v["001"]
        self.assertEqual(v1["name"], "001")
        self.assertEqual(v1.id, 538230818)
        self.assertEqual(v1.name, "001")
        self.assertEqual(v1.coordinate, (-24, -13))
        self.assertTrue(v1.is_main_village)
        with self.assertRaises(KeyError):
            v1["key error"]

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=village_raw
            )
            v1.pull()

        self.assertEqual(v1["name"], "001")
        self.assertEqual(v1.id, 536461288)
        self.assertEqual(v1.name, "001")
        self.assertEqual(v1.coordinate, (-24, -13))
        self.assertTrue(v1.is_main_village)
        with self.assertRaises(KeyError):
            v1["key error"]

    def testing_village_send_attack(self):
        g = None
        v = None
        villages_raw = {}
        raw_rally_point = {}
        raw_check_target = {}
        send_troops_raw = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/villages_raw.json", "r") as f:
            villages_raw = json.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with open("./tests/unit/fixtures/raw_check_target.json", "r") as f:
            raw_check_target = json.load(f)

        with open("./tests/unit/fixtures/send_troops_raw.json", "r") as f:
            send_troops_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=villages_raw
            )
            v = Villages(g)
            v.pull()

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": raw_rally_point},
                    {"json": raw_check_target},
                    {"json": send_troops_raw},
                ],
            )
            r = v["001"].send_attack(1, 1)
            self.assertEqual(r, send_troops_raw)

    def testing_village_send_raid(self):
        g = None
        v = None
        villages_raw = {}
        raw_rally_point = {}
        raw_check_target = {}
        send_troops_raw = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/villages_raw.json", "r") as f:
            villages_raw = json.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with open("./tests/unit/fixtures/raw_check_target.json", "r") as f:
            raw_check_target = json.load(f)

        with open("./tests/unit/fixtures/send_troops_raw.json", "r") as f:
            send_troops_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=villages_raw
            )
            v = Villages(g)
            v.pull()

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": raw_rally_point},
                    {"json": raw_check_target},
                    {"json": send_troops_raw},
                ],
            )
            r = v["001"].send_raid(1, 1)
            self.assertEqual(r, send_troops_raw)

    def testing_village_send_defend(self):
        g = None
        v = None
        villages_raw = {}
        raw_rally_point = {}
        raw_check_target = {}
        send_troops_raw = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/villages_raw.json", "r") as f:
            villages_raw = json.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with open("./tests/unit/fixtures/raw_check_target.json", "r") as f:
            raw_check_target = json.load(f)

        with open("./tests/unit/fixtures/send_troops_raw.json", "r") as f:
            send_troops_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=villages_raw
            )
            v = Villages(g)
            v.pull()

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": raw_rally_point},
                    {"json": raw_check_target},
                    {"json": send_troops_raw},
                ],
            )
            r = v["001"].send_defend(1, 1)
            self.assertEqual(r, send_troops_raw)

    def testing_village_send_spy(self):
        g = None
        v = None
        villages_raw = {}
        raw_rally_point = {}
        raw_check_target = {}
        send_troops_raw = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/villages_raw.json", "r") as f:
            villages_raw = json.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with open("./tests/unit/fixtures/raw_check_target.json", "r") as f:
            raw_check_target = json.load(f)

        with open("./tests/unit/fixtures/send_troops_raw.json", "r") as f:
            send_troops_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=villages_raw
            )
            v = Villages(g)
            v.pull()

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": raw_rally_point},
                    {"json": raw_check_target},
                    {"json": send_troops_raw},
                ],
            )
            r = v["001"].send_spy(1, 1)
            self.assertEqual(r, send_troops_raw)

    def testing_village_send_siege(self):
        g = None
        v = None
        villages_raw = {}
        raw_rally_point = {}
        raw_check_target = {}
        send_troops_raw = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/villages_raw.json", "r") as f:
            villages_raw = json.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with open("./tests/unit/fixtures/raw_check_target.json", "r") as f:
            raw_check_target = json.load(f)

        with open("./tests/unit/fixtures/send_troops_raw.json", "r") as f:
            send_troops_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=villages_raw
            )
            v = Villages(g)
            v.pull()

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": raw_rally_point},
                    {"json": raw_check_target},
                    {"json": send_troops_raw},
                ],
            )
            r = v["001"].send_siege(1, 1)
            self.assertEqual(r, send_troops_raw)

    def testing_village_send_farmlist(self):
        g = None
        v = None
        villages_raw = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/villages_raw.json", "r") as f:
            villages_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [{"json": villages_raw}, {"json": {"mock": "mocked"}}],
            )
            v = Villages(g)
            v.pull()
            r = v["001"].send_farmlist([123])

        self.assertEqual(r, {"mock": "mocked"})

    def testing_village_upgrade(self):
        g = None
        v = None
        villages_raw = {}
        village_raw = {}
        buildings_raw = {}
        building_queue_raw = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/villages_raw.json", "r") as f:
            villages_raw = json.load(f)

        with open("./tests/unit/fixtures/village_raw.json", "r") as f:
            village_raw = json.load(f)

        with open("./tests/unit/fixtures/buildings_raw.json", "r") as f:
            buildings_raw = json.load(f)

        with open("./tests/unit/fixtures/building_queue_raw.json", "r") as f:
            building_queue_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=villages_raw
            )
            v = Villages(g)
            v.pull()

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": {"mock": "mocked"}},
                ],
            )
            r = v["001"].upgrade(BuildingType.MAIN_BUILDING)

        self.assertEqual(r, {"mock": "mocked"})

        for x in buildings_raw["cache"][0]["data"]["cache"]:
            if x["data"]["buildingType"] == "1":
                x["data"]["upgradeCosts"] = {"1": 0, "2": 0, "3": 0, "4": 0}

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": {"mock": "mocked"}},
                ],
            )
            r = v["001"].upgrade(BuildingType.WOODCUTTER)

        self.assertEqual(r, {"mock": "mocked"})

        buildings_raw["cache"][0]["data"]["cache"][0]["data"]["upgradeCosts"][
            "1"
        ] = 999999999

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": {"mock": "mocked"}},
                ],
            )
            with self.assertRaises(WarehouseNotEnough):
                r = v["001"].upgrade(BuildingType.MAIN_BUILDING)

        v["001"].client.tribe_id = Tribe.ROMAN

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": {"mock": "mocked"}},
                ],
            )
            r = v["001"].upgrade(BuildingType.WOODCUTTER)

        self.assertEqual(r, {"mock": "mocked"})

        building_queue_raw["cache"][0]["data"]["freeSlots"]["2"] = 0

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": {"mock": "mocked"}},
                ],
            )
            r = v["001"].upgrade(BuildingType.WOODCUTTER)

        building_queue_raw["cache"][0]["data"]["freeSlots"]["4"] = 0

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": {"mock": "mocked"}},
                ],
            )
            with self.assertRaises(QueueFull):
                r = v["001"].upgrade(BuildingType.WOODCUTTER)

        buildings_raw["cache"][0]["data"]["cache"][0]["data"]["isMaxLvl"] = True

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": {"mock": "mocked"}},
                ],
            )
            with self.assertRaises(BuildingAtMaxLevel):
                r = v["001"].upgrade(BuildingType.MAIN_BUILDING)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": {"mock": "mocked"}},
                ],
            )
            with self.assertRaises(Exception):
                r = v["001"].upgrade(BuildingType.SMITHY)

    def testing_village_construct(self):
        g = None
        v = None
        villages_raw = {}
        village_raw = {}
        buildings_raw = {}
        building_queue_raw = {}
        construction_list_raw = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/villages_raw.json", "r") as f:
            villages_raw = json.load(f)

        with open("./tests/unit/fixtures/village_raw.json", "r") as f:
            village_raw = json.load(f)

        with open("./tests/unit/fixtures/buildings_raw.json", "r") as f:
            buildings_raw = json.load(f)

        with open("./tests/unit/fixtures/building_queue_raw.json", "r") as f:
            building_queue_raw = json.load(f)

        with open("./tests/unit/fixtures/construction_list_raw.json", "r") as f:
            construction_list_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=villages_raw
            )
            v = Villages(g)
            v.pull()

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": {"mock": "mocked"}},
                ],
            )
            with self.assertRaises(KeyError):
                r = v["001"].construct(BuildingType.STABLE)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": construction_list_raw},
                    {"json": {"mock": "mocked"}},
                ],
            )
            r = v["001"].construct(BuildingType.SMITHY)

        self.assertEqual(r, {"mock": "mocked"})

        construction_list_raw["response"]["buildings"]["buildable"][0][
            "upgradeCosts"
        ] = {"1": 0, "2": 0, "3": 0, "4": 0}

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": construction_list_raw},
                    {"json": {"mock": "mocked"}},
                ],
            )
            r = v["001"].construct(BuildingType.SMITHY)

        self.assertEqual(r, {"mock": "mocked"})

        construction_list_raw["response"]["buildings"]["buildable"][0][
            "upgradeCosts"
        ] = {"1": 0, "2": 0, "3": 0, "4": 9999999999}

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": construction_list_raw},
                    {"json": {"mock": "mocked"}},
                ],
            )
            with self.assertRaises(WarehouseNotEnough):
                r = v["001"].construct(BuildingType.SMITHY)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": construction_list_raw},
                    {"json": {"mock": "mocked"}},
                ],
            )
            with self.assertRaises(FailedConstructBuilding):
                r = v["001"].construct(BuildingType.STABLE)

        for x in buildings_raw["cache"][0]["data"]["cache"]:
            x["data"]["buildingType"] = "1"

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [
                    {"json": village_raw},
                    {"json": buildings_raw},
                    {"json": building_queue_raw},
                    {"json": construction_list_raw},
                ],
            )
            with self.assertRaises(BuildingSlotFull):
                r = v["001"].construct(BuildingType.SMITHY)


class TestWarehouse(unittest.TestCase):
    def testing_warehouse(self):
        g = None
        v = None
        villages_raw = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/villages_raw.json", "r") as f:
            villages_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=villages_raw
            )
            v = Villages(g)
            v.pull()

        v1 = v["001"]
        self.assertEqual(
            v1.warehouse.storage,
            {
                "1": 929.07843923224,
                "2": 712.9796366545,
                "3": 691.80224180989,
                "4": 641.28190453036,
            },
        )
        self.assertEqual(
            v1.warehouse.production, {"1": 1290, "2": 990, "3": 960, "4": 890}
        )
        self.assertEqual(
            v1.warehouse.capacity, {"1": 22500, "2": 22500, "3": 22500, "4": 15000}
        )
        self.assertEqual(v1.warehouse.wood, "929.07843923224/22500 1290")
        self.assertEqual(v1.warehouse.clay, "712.9796366545/22500 990")
        self.assertEqual(v1.warehouse.iron, "691.80224180989/22500 960")
        self.assertEqual(v1.warehouse.crop, "641.28190453036/15000 890")
        self.assertEqual(v1.warehouse["1"], 929.07843923224)
        self.assertEqual(v1.warehouse["wood"], 929.07843923224)
        with self.assertRaises(KeyError):
            v1.warehouse["key error"]


if __name__ == "__main__":
    unittest.main()
