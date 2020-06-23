from tkpy.map import cell_id
from tkpy.map import reverse_id
from tkpy.map import Map
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


class TestMap(unittest.TestCase):

    def testing_map(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            g = pickle.load(f)

        with open('./tests/unit/fixtures/map_raw.json', 'r') as f:
            fixtures_map = json.load(f)

        with open('./tests/unit/fixtures/map_raw2.json', 'r') as f:
            fixtures_map2 = json.load(f)

        with open('./tests/unit/fixtures/cell_details.json', 'r') as f:
            cell_details = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json=fixtures_map
            )

            m = Map(g)
            m.pull()

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json=cell_details
            )
            self.assertEqual(m.coordinate(0, 0).request_details()['resType'], '11115')

        self.assertEqual(m.coordinate(0, 0).id, cell_id(0, 0))
        self.assertEqual(m.coordinate(0, 0).coordinate.x, 0)
        self.assertEqual(m.coordinate(0, 0).coordinate.y, 0)
        self.assertEqual(m.coordinate(0, 0)['id'], str(cell_id(0, 0)))
        self.assertTrue('id' in m.coordinate(0, 0))

        self.assertEqual(len(list(m.gen_villages())), 2376)
        self.assertEqual(len(list(m.gen_abandoned_valley())), 5815)
        self.assertEqual(len(list(m.gen_oases())), 1226)
        self.assertEqual(len(list(m.gen_wilderness())), 26305)

        self.assertEqual(m.get_village('village not found?'), {})
        self.assertEqual(m.get_village(village_id=cell_id(-24, -13))['id'], str(cell_id(-24, -13)))

        self.assertEqual(m.coordinate(-111111, 111111), {})
        self.assertEqual(m.coordinate(0, 0)['id'], str(cell_id(0, 0)))
        with self.assertRaises(KeyError):
            m.coordinate(0, 0)['asdf']

        self.assertEqual(m.get_tile_by_id(123), {})
        self.assertEqual(m.get_tile_by_id(cell_id(0, 0)).id, cell_id(0, 0))

        self.assertEqual(len(list(m.gen_kingdoms())), 161)
        self.assertEqual(len(list(m.gen_players())), 1624)

        self.assertEqual(m.get_kingdom('BLA').id, '100')
        self.assertEqual(m.get_kingdom('BLA').name, 'BLA')
        self.assertEqual(m.get_kingdom('kingdom not found'), {})
        self.assertEqual(m.get_kingdom('BLA')['tag'], 'BLA')
        with self.assertRaises(KeyError):
            m.get_kingdom('BLA')['asdf']

        self.assertEqual(m.get_player('player not found'), {})
        self.assertEqual(m.get_player('Punisher').id, '119')
        self.assertEqual(m.get_player('Punisher').name, 'Punisher')
        self.assertEqual(m.get_player('Punisher')['name'], 'Punisher')
        self.assertEqual(m.get_player('Punisher').tribe_id, '1')
        self.assertTrue(m.get_player('Punisher').is_active)
        self.assertFalse(m.get_player('Mustafa').is_active)
        with self.assertRaises(KeyError):
            m.get_player('Punisher')['adsf']

        with open('./tests/unit/fixtures/hero_equipment.json', 'r') as f:
            hero_equipment = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json=hero_equipment
            )
            self.assertEqual(m.get_player('Punisher').request_hero_equipment()[0]['name'], 'HeroItem:20922')

        with open('./tests/unit/fixtures/player_details.json', 'r') as f:
            player_details = json.load(f)

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json=player_details
            )
            self.assertEqual(m.get_player('Punisher').request_details()['name'], 'Punisher')

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                'https://com1.kingdoms.com/api/',
                json=fixtures_map2
            )

            m = Map(g)
            m.pull_region_id([536461299])


if __name__ == '__main__':
    unittest.main()
