import unittest
import numpy as np
import pandas as pd
from pandas.testing import assert_frame_equal
from removeduplicates import migrate_params, render


def P(colnames=[], action='delete'):
    """Create params dict."""
    return {
        'colnames': colnames,
        'action': action,
    }


class MigrateParamsTest(unittest.TestCase):
    def test_migrate_params_v0_no_colnames(self):
        self.assertEqual(migrate_params({
            'colnames': '',
            'type': 0,
        }), {
            'colnames': [],
            'action': 'delete',
        })

    def test_migrate_params_v0(self):
        self.assertEqual(migrate_params({
            'colnames': 'A,B',
            'type': 0,
        }), {
            'colnames': ['A', 'B'],
            'action': 'delete',
        })

    def test_migrate_params_v0_cumcount(self):
        self.assertEqual(migrate_params({
            'colnames': 'A,B',
            'type': 1,
        }), {
            'colnames': ['A', 'B'],
            'action': 'cumcount',
        })

    def test_migrate_params_v1(self):
        self.assertEqual(migrate_params({
            'colnames': ['A', 'B'],
            'action': 'delete',
        }), {
            'colnames': ['A', 'B'],
            'action': 'delete',
        })


class RenderTest(unittest.TestCase):
    def test_delete_single_column_string(self):
        result = render(
            pd.DataFrame({
                'A': ['apple', 'apple', 'orange'],
                'B': ['monkey', 'kangaroo', 'cat'],
            }),
            P(['A'], 'delete')
        )
        expected = pd.DataFrame({'A': ['apple', 'orange'],
                                 'B': ['monkey', 'cat']})
        assert_frame_equal(result, expected)

    def test_delete_single_column_number(self):
        result = render(
            pd.DataFrame({'A': [0, 0, 1], 'B': ['monkey', 'kangaroo', 'cat']}),
            P(['A'], 'delete')
        )
        expected = pd.DataFrame({'A': [0, 1], 'B': ['monkey', 'cat']})
        assert_frame_equal(result, expected)

    def test_delete_unused_categories(self):
        result = render(
            pd.DataFrame({'A': ['a', 'b', 'c'], 'B': ['d', 'd', 'e']},
                         dtype='category'),
            P(['B'], 'delete')
        )
        expected = pd.DataFrame({'A': ['a', 'c'], 'B': ['d', 'e']},
                                dtype='category')
        assert_frame_equal(result, expected)

    def test_delete_multi_column(self):
        result = render(
            pd.DataFrame({
                'A': ['apple', 'apple', 'orange'],
                'B': [0, 0, 'cat'],
                'C': ['monkey', 'kangaroo', 'cat'],
            }),
            P(['A', 'B'], 'delete')
        )
        expected = pd.DataFrame({
            'A': ['apple', 'orange'],
            'B': [0, 'cat'],
            'C': ['monkey', 'cat'],
        })
        assert_frame_equal(result, expected)

    def test_cumcount_single_column_string(self):
        result = render(
            pd.DataFrame({'A': ['apple', 'apple', 'orange'],
                          'B': ['monkey', 'kangaroo', 'cat']}),
            P(['A'], 'cumcount')
        )
        expected = pd.DataFrame({
            'A': ['apple', 'apple', 'orange'],
            'B': ['monkey', 'kangaroo', 'cat'],
            'Duplicate number': [1, 2, 1]
        })
        assert_frame_equal(result, expected)

    def test_cumcount_single_column_number(self):
        result = render(
            pd.DataFrame({'A': [0, 0, 1], 'B': ['monkey', 'kangaroo', 'cat']}),
            P(['A'], 'cumcount')
        )
        expected = pd.DataFrame({
            'A': [0, 0, 1],
            'B': ['monkey', 'kangaroo', 'cat'],
            'Duplicate number': [1, 2, 1]
        })
        assert_frame_equal(result, expected)

    def test_cumcount_multi_column(self):
        result = render(
            pd.DataFrame({
                'A': ['apple', 'orange', 'apple'],
                'B': [0, 'kangaroo', 0],
                'C': ['monkey', 'kangaroo', 'cat'],
            }),
            P(['A', 'B'], 'cumcount')
        )
        expected = pd.DataFrame({
            'A': ['apple', 'orange', 'apple'],
            'B': [0, 'kangaroo', 0],
            'C': ['monkey', 'kangaroo', 'cat'],
            'Duplicate number': [1, 1, 2]
        })
        assert_frame_equal(result, expected)

    def test_no_colnames(self):
        # No colnames -> do nothing
        result = render(
            pd.DataFrame({'A': ['', np.nan, 'x']}),
            P([], 'delete')
        )
        expected = pd.DataFrame({'A': ['', np.nan, 'x']})
        assert_frame_equal(result, expected)


if __name__ == '__main__':
    unittest.main()
