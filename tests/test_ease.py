import unittest

from ..ease import Ease


# In the upper directory of pytweener, run the test with the following command.
# python -m unittest pytweener.tests.test_ease -v


functions = [
    'linear',
    'in_sine',
    'out_sine',
    'in_out_sine',
    'in_cubic',
    'out_cubic',
    'in_out_cubic',
    'in_quint',
    'out_quint',
    'in_out_quint',
    'in_circ',
    'out_circ',
    'in_out_circ',
    'in_elastic',
    'out_elastic',
    'in_out_elastic',
    'in_quad',
    'out_quad',
    'in_out_quad',
    'in_quart',
    'out_quart',
    'in_out_quart',
    'in_expo',
    'out_expo',
    'in_out_expo',
    'in_back',
    'out_back',
    'in_out_back',
    'in_bounce',
    'out_bounce',
    'in_out_bounce'
]


class TestEase(unittest.TestCase):

    def test_in_sine(self):
        tests = [
            [0.0, 0.0],
            [1.0, 1.0]
        ]

        for func_name in functions:
            func = getattr(Ease, func_name)

            for t, expect in tests:
                with self.subTest((func_name, t)):
                    result = func(t)
                    self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()