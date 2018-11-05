import unittest
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from removeduplicates import removeduplicates, render

count_col_name = 'Cumulative count'

class TestRemoveDuplicates(unittest.TestCase):
    def test_remove_single_column_string(self):
        result = pd.DataFrame({'A': ['apple', 'apple', 'orange'], 'B': ['monkey', 'kangaroo', 'cat']})
        result = removeduplicates(result, ['A'], 0)
        expected = pd.DataFrame({'A': ['apple', 'orange'], 'B': ['monkey', 'cat']})
        assert_frame_equal(result, expected)

    def test_remove_single_column_number(self):
        result = pd.DataFrame({'A': [0, 0, 1], 'B': ['monkey', 'kangaroo', 'cat']})
        result = removeduplicates(result, ['A'], 0)
        expected = pd.DataFrame({'A': [0, 1], 'B': ['monkey', 'cat']})
        assert_frame_equal(result, expected)

    def test_remove_multi_column(self):
        result = pd.DataFrame({'A': ['apple', 'apple', 'orange'], 'B': [0, 0, 'cat'], 'C': ['monkey', 'kangaroo', 'cat']})
        result = removeduplicates(result, ['A', 'B'], 0)
        expected = pd.DataFrame({'A': ['apple', 'orange'], 'B': [0, 'cat'], 'C': ['monkey', 'cat']})
        assert_frame_equal(result, expected)

    def test_count_single_column_string(self):
        result = pd.DataFrame({'A': ['apple', 'apple', 'orange'], 'B': ['monkey', 'kangaroo', 'cat']})
        result = removeduplicates(result, ['A'], 1)
        expected = pd.DataFrame({'A': ['apple', 'apple', 'orange'], 'B': ['monkey', 'kangaroo', 'cat'], count_col_name: [1, 2, 1]})
        assert_frame_equal(result, expected)

    def test_count_single_column_number(self):
        result = pd.DataFrame({'A': [0, 0, 1], 'B': ['monkey', 'kangaroo', 'cat']})
        result = removeduplicates(result, ['A'], 1)
        expected = pd.DataFrame({'A': [0, 0, 1], 'B': ['monkey', 'kangaroo', 'cat'], count_col_name: [1, 2, 1]})
        assert_frame_equal(result, expected)

    def test_count_multi_column(self):
        result = pd.DataFrame({'A': ['apple', 'orange', 'apple'], 'B': [0, 'kangaroo', 0], 'C': ['monkey', 'kangaroo', 'cat']})
        result = removeduplicates(result, ['A'], 1)
        expected = pd.DataFrame({'A': ['apple', 'orange', 'apple'], 'B': [0, 'kangaroo', 0],
                                 'C': ['monkey', 'kangaroo', 'cat'], count_col_name: [1, 1, 2]})
        assert_frame_equal(result, expected)

class RenderTest(unittest.TestCase):
    def test_no_colnames(self):
        # No colnames -> do nothing
        result = pd.DataFrame({'A': ['', np.nan, 'x']})
        result = render(result, {'colnames': '', 'type': 0})
        expected = pd.DataFrame({'A': ['', np.nan, 'x']})
        assert_frame_equal(result, expected)

    def test_colnames_comma_separated(self):
        result = pd.DataFrame({
            'A': ['a', 'a', 'c'],
            'B': ['a', 'a', 'c'],
            'C': ['a', 'y', 'z'],
        })
        result = render(result, {'colnames': 'A,B', 'type': 0})
        expected = pd.DataFrame({'A': ['a', 'c'], 'B': ['a', 'c'], 'C': ['a', 'z']})
        assert_frame_equal(result, expected)

    def test_missing_colname(self):
        result = pd.DataFrame({'A': [1]})
        result = render(result, {'colnames': 'B', 'type': 0})
        self.assertEqual(result, 'You chose a missing column')


if __name__ == '__main__':
    unittest.main()
