from tkpy.rally_point import RallyPoint
from tkpy.enums.tribe import Tribe
from tkpy.enums.troop import RomanTroop
from tkpy.enums.troop import TeutonTroop
from tkpy.enums.troop import GaulTroop
from tkpy.exception import TargetNotFound
import unittest
import requests_mock
import pickle
import json


class TestRallyPoint(unittest.TestCase):
    #  def testing_rally_point_property(self):
    #  g = None
    #  r = None
    #  raw_rally_point = {}

    #  with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
    #  g = pickle.load(f)

    #  with open('./tests/unit/fixtures/raw_rally_point.json', 'r') as f:
    #  raw_rally_point = json.load(f)

    #  with requests_mock.mock() as mock:
    #  mock.register_uri(
    #  "POST", "https://com1.kingdoms.com/api/", json=raw_rally_point
    #  )
    #  r = RallyPoint(g, "538230818")
    #  r.pull()

    #  self.assertEqual(r.unit_available, raw_rally_point["cache"][0]["data"]["cache"][0]["data"])

    def testing_rally_point_target_not_found(self):
        g = None
        rp = None
        raw_rally_point = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=raw_rally_point
            )
            rp = RallyPoint(g, "538230818")
            rp.pull()

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST",
                "https://com1.kingdoms.com/api/",
                json={"response": {"errors": "error just happened"}},
            )
            with self.assertRaises(TargetNotFound):
                r = rp.send_attack(0, 0)

    def testing_rally_point_send_no_troop(self):
        g = None
        rp = None
        raw_rally_point = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=raw_rally_point
            )
            rp = RallyPoint(g, "538230818")
            rp.pull()

        with self.assertRaises(SyntaxError):
            r = rp.send_attack(0, 0, {RomanTroop.LEGIONNAIRE: 0})

    def testing_rally_point_send_more_troop(self):
        g = None
        rp = None
        raw_rally_point = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=raw_rally_point
            )
            rp = RallyPoint(g, "538230818")
            rp.pull()

        with self.assertRaises(SyntaxError):
            r = rp.send_attack(0, 0, {TeutonTroop.CLUBSWINGER: 9999999999})

    def testing_rally_point_send_siege_with_ram(self):
        g = None
        rp = None
        raw_rally_point = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=raw_rally_point
            )
            rp = RallyPoint(g, "538230818")
            rp.pull()

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json={"mock": "mocked"}
            )
            r = rp.send_siege(
                0,
                0,
                {RomanTroop.LEGIONNAIRE: 1000, RomanTroop.BATTERING_RAM: 1},
                check_target=False,
            )

        self.assertEqual(r, {"mock": "mocked"})

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json={"mock": "mocked"}
            )
            r = rp.send_siege(
                0, 0, {GaulTroop.PHALANX: 1000, GaulTroop.RAM: 1}, check_target=False
            )

        self.assertEqual(r, {"mock": "mocked"})

    def testing_rally_point_send_siege_without_ram(self):
        g = None
        rp = None
        raw_rally_point = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=raw_rally_point
            )
            rp = RallyPoint(g, "538230818")
            rp.pull()

        with self.assertRaises(SyntaxError):
            r = rp.send_siege(0, 0, {GaulTroop.PHALANX: 1000}, check_target=False)

    def testing_rally_point_send_attack_all_scout(self):
        g = None
        rp = None
        raw_rally_point = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=raw_rally_point
            )
            rp = RallyPoint(g, "538230818")
            rp.pull()

        with self.assertRaises(SyntaxError):
            r = rp.send_attack(0, 0, {RomanTroop.EQUITES_LEGATI: 10})

        with self.assertRaises(SyntaxError):
            r = rp.send_attack(0, 0, {TeutonTroop.SCOUT: 10})

        with self.assertRaises(SyntaxError):
            r = rp.send_attack(0, 0, {GaulTroop.PATHFINDER: 10})

    def testing_rally_point_send_raid_all_scout(self):
        g = None
        rp = None
        raw_rally_point = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=raw_rally_point
            )
            rp = RallyPoint(g, "538230818")
            rp.pull()

        with self.assertRaises(SyntaxError):
            r = rp.send_raid(0, 0, {RomanTroop.EQUITES_LEGATI: 10})

    def testing_rally_point_send_spy_error_mission(self):
        g = None
        rp = None
        raw_rally_point = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=raw_rally_point
            )
            rp = RallyPoint(g, "538230818")
            rp.pull()

        with self.assertRaises(SyntaxError):
            r = rp.send_spy(0, 0, 1, "error")

    def testing_rally_point_send_spy_using_another_tribe(self):
        g = None
        rp = None
        raw_rally_point = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=raw_rally_point
            )
            rp = RallyPoint(g, "538230818")
            rp.pull()

        rp.client.tribe_id = Tribe.ROMAN

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json={"mock": "mocked"}
            )
            r = rp.send_spy(0, 0, 1, check_target=False)

        self.assertEqual(r, {"mock": "mocked"})

        rp.client.tribe_id = Tribe.GAUL

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json={"mock": "mocked"}
            )
            r = rp.send_spy(0, 0, 1, check_target=False)

        self.assertEqual(r, {"mock": "mocked"})

    def testing_rally_point_send_siege_all_scout(self):
        g = None
        rp = None
        raw_rally_point = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=raw_rally_point
            )
            rp = RallyPoint(g, "538230818")
            rp.pull()

        with self.assertRaises(SyntaxError):
            r = rp.send_siege(0, 0, {RomanTroop.EQUITES_LEGATI: 10})

    def testing_rally_point_send_siege_less_than_1k(self):
        g = None
        rp = None
        raw_rally_point = {}

        with open("./tests/unit/fixtures/pickled_driver.py", "rb") as f:
            g = pickle.load(f)

        with open("./tests/unit/fixtures/raw_rally_point.json", "r") as f:
            raw_rally_point = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                "POST", "https://com1.kingdoms.com/api/", json=raw_rally_point
            )
            rp = RallyPoint(g, "538230818")
            rp.pull()

        with self.assertRaises(SyntaxError):
            r = rp.send_siege(0, 0, {RomanTroop.LEGIONNAIRE: 10})
