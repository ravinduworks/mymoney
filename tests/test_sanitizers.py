import unittest

from src.sanitization import DataSanitizer


class TestDataConverters(unittest.TestCase):
    def test_returns_list(self):
        data = 'CHANGE 11.00% 9.00% 4.00% JANUARY'
        self.assertEqual(type(DataSanitizer.clean_command(data)), list)

    def test_removes_new_lines(self):
        data = 'CHANGE 11.00% 9.00% 4.00% JANUARY\n'
        self.assertTrue('\n' not in DataSanitizer.clean_command(data), True)

    def test_removes_percentages(self):
        data = 'CHANGE 11.00% 9.00% 4.00% JANUARY'
        self.assertTrue('%' not in DataSanitizer.clean_command(data), True)


if __name__ == '__main__':
    unittest.main()
