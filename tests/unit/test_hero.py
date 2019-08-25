from tkpy.hero import Hero
from tkpy.exception import NotEnoughAdventurePoint
from tkpy.exception import HeroNotInHome

import unittest
import requests_mock
import pickle
import json


class TestHero(unittest.TestCase):

    def setUp(self):
        with open('./tests/unit/fixtures/pickled_driver.py', 'rb') as f:
            self.g = pickle.load(f)

        with open('./tests/unit/fixtures/hero_raw.json', 'r') as f:
            self.hero_raw = json.load(f)

        self.url = 'https://com93.kingdoms.com/api/'

        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json=self.hero_raw
            )
            self.hero = Hero(client=self.g)
            self.hero.pull()

    def testing_hero_attribute(self):
        self.assertEqual(self.hero.playerId, '1')
        self.assertEqual(self.hero.villageId, '1')
        self.assertEqual(self.hero.destVillageId, '1')
        self.assertEqual(self.hero.level, '1')
        self.assertEqual(self.hero.xpThisLevel, 500)
        self.assertEqual(self.hero.xpNextLevel, 750)
        self.assertEqual(self.hero.adventurePoints, '1')
        self.assertEqual(self.hero.freePoints, '0')
        self.assertFalse(self.hero.isMoving)
        self.assertEqual(self.hero.regenerationRate, 15)
        self.assertEqual(self.hero.status, '7') # die
        self.assertEqual(self.hero.health, '0')
        # property
        self.assertEqual(self.hero.exp, 242)
        self.assertEqual(self.hero.exp_next_level, 250)
        self.assertFalse(self.hero.in_home)

    def testing_hero_adventures(self):
        self.hero.data.update({'status': '0'})
        with requests_mock.mock() as mock:
            mock.register_uri(
                'POST',
                self.url,
                json={'mock': 'mocked'}
            )
            r = self.hero.adventures('short')
        self.assertEqual(r, {'mock': 'mocked'})

    def testing_hero_adventures_raises_not_enough_adventure_points(self):
        self.hero.data.update({'adventurePoints': '0'})
        with self.assertRaises(NotEnoughAdventurePoint):
            self.hero.adventures('short')

    def testing_hero_adventures_raises_hero_not_in_home(self):
        with self.assertRaises(HeroNotInHome):
            self.hero.adventures('short')


if __name__ == '__main__':
    unittest.run()
