from tkpy.buildings import Buildings
from tkpy.buildings import BuildingQueue
from tkpy.buildings import ConstructionList
from tkpy.enums.building import BuildingType
import unittest
import requests_mock
import pickle
import json


class TestBuildings(unittest.TestCase):
    def testing_buildings(self):
        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/buildings_raw.json", "r") as f:
            buildings_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=buildings_raw
            )
            b = Buildings(g, 536461288)
            b.pull()
        self.assertEqual(len(b[BuildingType.CROPLAND]), 6)
        self.assertEqual(len(b.freeSlots), 8)
        self.assertEqual(len(list(b.raw)), 40)
        self.assertEqual(b[BuildingType.CROPLAND][0].id, "4")
        self.assertEqual(b[BuildingType.CROPLAND][0]["buildingType"], "4")
        self.assertEqual(b[BuildingType.CROPLAND][0].location, "2")
        self.assertEqual(b[BuildingType.CROPLAND][0].lvl, 6)
        self.assertFalse(b[BuildingType.CROPLAND][0].is_max_level)
        self.assertEqual(
            b[BuildingType.CROPLAND][0].upgrade_cost,
            {"1": 1625, "2": 1950, "3": 1845, "4": 0},
        )
        with self.assertRaises(KeyError):
            b[BuildingType.CROPLAND][0]["KeyError"]

        with self.assertRaises(TypeError):
            b["NotABuildingType"]

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json={"mock": "mocked"}
            )
            r = b[BuildingType.CROPLAND][0].upgrade()
            self.assertEqual(r, {"mock": "mocked"})
            r = b[BuildingType.CROPLAND][0].queues(reserveResources=False)
            self.assertEqual(r, {"mock": "mocked"})

    def testing_building_queue(self):
        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/building_queue_raw.json", "r") as f:
            building_queue_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=building_queue_raw
            )
            bq = BuildingQueue(g, 536461288)
            bq.pull()
        self.assertEqual(bq.freeSlots, {"1": 1, "2": 1, "4": 1})
        self.assertEqual(bq.queues, {"1": [], "2": [], "4": [], "5": []})

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json={"mock": "mocked"}
            )
            r = bq.finishNow(2)
            self.assertEqual(r, {"mock": "mocked"})

    def testing_construction_list(self):
        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/construction_list_raw.json", "r") as f:
            construction_list_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=construction_list_raw
            )
            c = ConstructionList(g, 536461288, "39")
            c.pull()
        self.assertEqual(len(c.buildable), 4)
        self.assertEqual(len(c.notBuildable), 8)
        with self.assertRaises(KeyError):
            c[BuildingType.CRANNY]
        self.assertFalse(c[BuildingType.IRON_FOUNDRY]["buildable"])
        self.assertTrue(c[BuildingType.SMITHY]["buildable"])
        with self.assertRaises(KeyError):
            c[BuildingType.SMITHY]["keyError"]

        with self.assertRaises(TypeError):
            c["NotABuildingType"]


if __name__ == "__main__":
    unittest.main()
