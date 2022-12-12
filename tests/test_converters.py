import unittest

from src.conversion import DataConverter


class TestDataConverters(unittest.TestCase):
    def test_convert_to_int(self):
        data = ['1', '2', '3', '4']
        self.assertEqual(
            DataConverter.convert_to_int(data),
            [
                1,
                2,
                3,
                4,
            ],
        )

    def test_convert_to_float(self):
        data = ['1.0', '2.0', '3.0', '4.0']
        self.assertEqual(
            DataConverter.convert_to_float(data),
            [
                1.0,
                2.0,
                3.0,
                4.0,
            ],
        )

    def test_convert_with_empty(self):
        data = []
        self.assertEqual(DataConverter.convert_to_float(data), [])
        self.assertEqual(DataConverter.convert_to_int(data), [])


if __name__ == '__main__':
    unittest.main()
