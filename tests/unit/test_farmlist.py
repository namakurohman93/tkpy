from tkpy.farmlist import Farmlist
from tkpy.exception import FarmListNotFound
import unittest
import requests_mock
import pickle
import json


class TestFarmlist(unittest.TestCase):
    def testing_farmlist(self):
        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/farmlist_raw.json", "r") as f:
            farmlist_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=farmlist_raw
            )
            fl = Farmlist(g)
            fl.pull()
        self.assertEqual(len(list(fl.raw)), 3)
        self.assertEqual(len(list(fl.list)), 3)
        self.assertEqual(fl["01"]["listName"], "01")
        with self.assertRaises(FarmListNotFound):
            fl["farmlist not found"]

        farmlist_raw["cache"][0]["data"]["cache"].append(
            farmlist_raw["cache"][0]["data"]["cache"][2]
        )
        farmlist_raw["cache"][0]["data"]["cache"][3]["data"]["listName"] = "test"

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [{"json": {"mock": "mocked"}}, {"json": farmlist_raw}],
            )
            fl.create_farmlist("test")
            self.assertEqual(fl["test"]["listName"], "test")


class TestFarmlistEntry(unittest.TestCase):
    def testing_farmlist_entry(self):
        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/farmlist_raw.json", "r") as f:
            farmlist_raw = json.load(f)

        with open("./tests/unit/fixtures/farmlist_entry_raw.json", "r") as f:
            farmlist_entry_raw = json.load(f)

        with open("./tests/unit/fixtures/farmlist_entry_pull_raw.json", "r") as f:
            farmlist_entry_pull_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=farmlist_raw
            )
            fl = Farmlist(g)
            fl.pull()
        fe = fl["01"]
        self.assertEqual(fe.name, "01")
        self.assertEqual(fe.id, 1398)
        self.assertEqual(len(fe.villageIds), 10)
        self.assertEqual(len(fe.entryIds), 10)
        with self.assertRaises(KeyError):
            fe["key error"]

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json={"mock": "mocked"}
            )
            r = fe.send(123)
            self.assertEqual(r, {"mock": "mocked"})

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=farmlist_entry_raw
            )
            fe.add(535150570)
            self.assertEqual(len(fe.villageIds), 11)
            self.assertTrue("535150570" in fe.villageIds)
            self.assertEqual(len(fe.entryIds), 11)
            fe.toggle(535150570)
            self.assertEqual(len(fe.villageIds), 11)
            self.assertTrue("535150570" in fe.villageIds)
            self.assertEqual(len(fe.entryIds), 11)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=farmlist_entry_pull_raw
            )
            fe.pull()
            self.assertEqual(len(list(fe.farmlistEntry)), 11)


class TestEntryId(unittest.TestCase):
    def testing_entry_id(self):
        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/farmlist_raw.json", "r") as f:
            farmlist_raw = json.load(f)

        with open("./tests/unit/fixtures/farmlist_entry_pull_raw.json", "r") as f:
            farmlist_entry_pull_raw = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                [{"json": farmlist_raw}, {"json": farmlist_entry_pull_raw}],
            )
            fl = Farmlist(g)
            fl.pull()
            fl["01"].pull()
        fl_list = list(fl["01"].farmlistEntry)
        ei = fl_list[0]
        self.assertEqual(ei.id, "6350")
        self.assertEqual(ei["entryId"], "6350")
        self.assertEqual(ei.villageId, "535150570")
        self.assertEqual(ei.notificationType, "0")
        self.assertEqual(ei.raidedSum, 0)
        self.assertEqual(ei.capacity, 0)
        with self.assertRaises(KeyError):
            ei["key error"]

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json={"mock": "mocked"}
            )
            ei.copy(123)
            ei.delete()


if __name__ == "__main__":
    unittest.main()
