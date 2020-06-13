from tkpy.models import CustomizeDict
from tkpy.models import ImmutableDataclass

import unittest


class TestCustomizeDict(unittest.TestCase):

    def testing_immutable_dict(self):
        d = CustomizeDict({'a':'a', 'b':'b', 'c':'c'})
        with self.assertRaises(TypeError):
            d['a'] = 'z'
        with self.assertRaises(TypeError):
            d['z'] = 'z'


class TestImmutableDataclass(unittest.TestCase):

    def testing_immutable_data_class(self):
        d = ImmutableDataclass({'a':'a', 'b':'b', 'c':'c'}, safe=[])
        self.assertEqual(d.a, 'a')
        self.assertEqual(d['a'], 'a')
        with self.assertRaises(TypeError):
            d['a'] = 'z'
        self.assertEqual(dir(d), ['a', 'b', 'c', 'data'])
        self.assertTrue('a' in d)


if __name__ == '_main__':
    unittest.run()
