import unittest
from pureFunc import getFormatedName


class NameTesstCase(unittest.TestCase):
    def test_first_last_name(self):
        formatName = getFormatedName("peizhong", "wang")
        self.assertEqual(formatName, "Peizhong Wang")

    def test_multi_name(self):
        formatName = getFormatedName("peizhong", "wang", "xxx")
        self.assertEqual(formatName, "Peizhong Wang")


unittest.main()
