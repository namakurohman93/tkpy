from tkpy.map import cell_id
from tkpy.map import reverse_id
from tkpy.map import Map
from tkpy.map import Point
import requests_mock
import unittest
import pickle
import json


class TestCellId(unittest.TestCase):

    def testing_cell_id_function(self):
        self.assertEqual(cell_id(0, 1), 536920064)
        self.assertNotEqual(cell_id(0, 0), 0)


class TestReverseId(unittest.TestCase):

    def testing_reverse_id_function(self):
        self.assertEqual(reverse_id(536920064), (0, 1))
        self.assertNotEqual(reverse_id(536920064), (0, 0))
        self.assertEqual(reverse_id(cell_id(0, -99)), (0, -99))


class TestPoint(unittest.TestCase):

    def testing_point(self):
        p1 = Point(0, 0)
        p2 = Point(0, 1)
        p3 = Point.from_cell_id(cell_id(0, 0))
        d1 = p1 >> p2
        d2 = (0, 1) >> p1
        d3 = {'x': 0, 'y': 1} >> p1

        self.assertEqual(p1.id, p3.id)
        self.assertEqual(d1, 1)
        self.assertEqual(p1.distance_to(0, 1), d1)
        self.assertEqual(d2, 1)
        self.assertEqual(d3, 1)
        with self.assertRaises(TypeError):
            'mock' >> p1


class TestMap(unittest.TestCase):

    def setUp(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            self.g = pickle.load(f)

        with open('./tests/unit/fixtures/map_raw.json', 'r') as f:
            self.fixtures_map = json.load(f)

        with open('./tests/unit/fixtures/map_raw2.json', 'r') as f:
            self.fixtures_map2 = json.load(f)

        with open('./tests/unit/fixtures/cell_details.json', 'r') as f:
            self.cell_details = json.load(f)

        with open('./tests/unit/fixtures/hero_equipment.json', 'r') as f:
            self.hero_equipment = json.load(f)

        with open('./tests/unit/fixtures/player_details.json', 'r') as f:
            self.player_details = json.load(f)

    def testing_map(self):

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json=self.fixtures_map
            )

            m = Map(self.g)
            m.pull()

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json=self.cell_details
            )
            self.assertEqual(m.coordinate(0, 0).details()['resType'], '11115')

        self.assertEqual(m.coordinate(0, 0).id, cell_id(0, 0))
        self.assertEqual(m.coordinate(0, 0).coordinate.x, 0)
        self.assertEqual(m.coordinate(0, 0)['id'], cell_id(0, 0))
        self.assertTrue('id' in m.coordinate(0, 0))

        self.assertEqual(len(list(m.villages)), 2376)
        self.assertEqual(len(list(m.tiles)), 5815)
        self.assertEqual(len(list(m.oasis)), 1226)
        self.assertEqual(len(list(m.wilderness)), 26305)

        self.assertEqual(m.coordinate(-111111, 111111), {})
        self.assertEqual(m.coordinate(0, 0)['id'], cell_id(0, 0))
        with self.assertRaises(KeyError):
            m.coordinate(0, 0)['asdf']

        self.assertEqual(m.tile(123), {})
        self.assertEqual(m.tile(cell_id(0, 0)).id, cell_id(0, 0))

        self.assertEqual(len(list(m.kingdoms)), 161)
        self.assertEqual(len(list(m.players)), 1624)

        self.assertEqual(m.kingdom('BLA').id, '100')
        self.assertEqual(m.kingdom('BLA').name, 'BLA')
        self.assertEqual(m.kingdom('kingdom not found'), {})
        self.assertEqual(m.kingdom('BLA')['tag'], 'BLA')
        with self.assertRaises(KeyError):
            m.kingdom('BLA')['asdf']

        self.assertEqual(m.player('player not found'), {})
        self.assertEqual(m.player('Punisher').id, '119')
        self.assertEqual(m.player(id=119).id, '119')
        self.assertEqual(m.player(), {})
        self.assertEqual(m.player('Punisher').name, 'Punisher')
        self.assertEqual(m.player('Punisher')['name'], 'Punisher')
        self.assertEqual(m.player('Punisher').tribeId, 1)
        self.assertTrue(m.player('Punisher').is_active)
        self.assertFalse(m.player('Mustafa').is_active)
        with self.assertRaises(KeyError):
            m.player('Punisher')['adsf']

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json=self.hero_equipment
            )
            self.assertEqual(m.player('Punisher').hero_equipment()[0]['name'], 'HeroItem:20922')

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json=self.player_details
            )
            self.assertEqual(m.player('Punisher').details()['name'], 'Punisher')

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com93.kingdoms.com/api/',
                json=self.fixtures_map2
            )

            m = Map(self.g)
            m.pull([536461299])


if __name__ == '__main__':
    unittest.main()
