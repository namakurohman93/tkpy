from tkpy.map import cell_id
from tkpy.map import distance
from tkpy.map import reverse_id
import unittest


class TestDistance(unittest.TestCase):

    def testing_distance_function(self):
        self.assertEqual(distance((0,0), (0,3)), 3)
        self.assertNotEqual(distance((0,0), (0,3)), 4)


class TestCellId(unittest.TestCase):

    def testing_cell_id_function(self):
        self.assertEqual(cell_id(0, 1), 536920064)
        self.assertNotEqual(cell_id(0, 0), 0)


class TestReverseId(unittest.TestCase):

    def testing_reverse_id_function(self):
        self.assertEqual(reverse_id(536920064), (0, 1))
        self.assertNotEqual(reverse_id(536920064), (0, 0))


if __name__ == '__main__':
    unittest.main()
