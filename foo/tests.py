import unittest
from foo.DataContext import QueryBaseinfoConfig, SetBaseinfoBuffer, GetBaseinfoBuffer

'''
python -m unittest test_module1 test_module2
python -m unittest test_module.TestClass
python -m unittest test_module.TestClass.test_method
'''


class RedisTestCase(unittest.TestCase):

    def test_get_local_data(self):
        result = QueryBaseinfoConfig()
        self.assertTrue(len(result) > 0)
        result = QueryBaseinfoConfig('104')
        self.assertTrue(len(result) > 0)

    def test_set_hash(self):
        src = SetBaseinfoBuffer()
        self.assertTrue(src > 0)

    def test_get_hash(self):
        res = GetBaseinfoBuffer()
        print(res)
        self.assertTrue(res > 0)


if __name__ == '__main__':
    unittest.main()
