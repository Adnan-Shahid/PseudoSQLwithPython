import unittest
from squeal import *
from database import *


class TestCartesianProduct(unittest.TestCase):
    def test_format(self):

        dict1 = {'title': ['m1', 'm2'], 'year': ['5', '6']}
        dict2 = {'t': ['m1', 'm2', 'm3'], 'y': ['5', '6', '7'],
                 'money': ['1.0', '2.0', '3.0']}
        table1 = Table()
        table2 = Table()
        table1.set_dict(dict1)
        table2.set_dict(dict2)
        result_table = cartesian_product(table1, table2)
        result_dict = result_table.get_dict()
        expected_dict = {'t': ['m1', 'm2', 'm3', 'm1', 'm2', 'm3'],
                         'title': ['m1', 'm1', 'm1', 'm2', 'm2', 'm2'],
                         'year': ['5', '5', '5', '6', '6', '6'],
                         'y': ['5', '6', '7', '5', '6', '7'],
                         'money': ['1.0', '2.0', '3.0', '1.0', '2.0', '3.0']}

        self.assertEqual(result_dict, expected_dict,
                         "cartesian_product was not coded properly")

    def test_order(self):
        dict1 = {'k1': 'a', 'b': 'c'}
        dict2 = {'k3': ['1', '2', '3'], 'k4': ['4', '5', '6'],
                 'k5': ['7', '8', '9']}
        table1 = Table()
        table2 = Table()
        table1.set_dict(dict1)
        table2.set_dict(dict2)
        result_table = cartesian_product(table1, table2)
        result_dict = result_table.get_dict()
        expected_dict = {'k1': ['a', 'a', 'a'], 'k4': ['4', '5', '6'],
                         'k5': ['7', '8', '9'], 'b': ['c', 'c', 'c'],
                         'k3': ['1', '2', '3']}
        self.assertEqual(result_dict, expected_dict,
                         "d1 or d2 must be of the following form:" +
                         "key: list of values")

    def test_key_type_float(self):
        dict1 = {1.0: ['as'], 2.0: ['da']}
        dict2 = {'title': ['m1', 'm2'], 'year': ['5', '6']}
        table1 = Table()
        table2 = Table()
        table1.set_dict(dict1)
        table2.set_dict(dict2)
        result_table = cartesian_product(table1, table2)
        result_dict = result_table.get_dict()
        expected_dict = {1.0: ['as', 'as'], 2.0: ['da', 'da'],
                         'year': ['5', '6'], 'title': ['m1', 'm2']}

        self.assertEqual(result_dict, expected_dict, "a key can = a float")

    def test_key_type_bool(self):
            dict1 = {False: ['2'], True: ['asd']}
            dict2 = {'title': ['m1', 'm2'], 'year': ['5', '6']}
            table1 = Table()
            table2 = Table()
            table1.set_dict(dict1)
            table2.set_dict(dict2)
            result_table = cartesian_product(table1, table2)
            result_dict = result_table.get_dict()
            expected_dict = {False: ['2', '2'], True: ['asd', 'asd'],
                             'year': ['5', '6'], 'title': ['m1', 'm2']}
            self.assertEqual(result_dict, expected_dict, "bools can be keys")

    def test_key_type_int(self):
            dict1 = {5: ['6'], 7: ['8']}
            dict2 = {'title': ['m1', 'm2'], 'year': ['5', '6']}
            table1 = Table()
            table2 = Table()
            table1.set_dict(dict1)
            table2.set_dict(dict2)
            result_table = cartesian_product(table1, table2)
            result_dict = result_table.get_dict()
            expected_dict = {'title': ['m1', 'm2'], 7: ['8', '8'],
                             5: ['6', '6'], 'year': ['5', '6']}
            self.assertEqual(result_dict, expected_dict, "ints can be keys")

unittest.main(exit=False)
