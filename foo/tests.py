import unittest
from foo.DataContext import QueryBaseinfoConfig, SetBaseinfoBuffer, GetBaseinfoBuffer, SetNewPocast
from foo.Mail import sendMail, sendNewFile
'''
python -m unittest foo.tests.MailTestCase
python -m unittest foo.tests.RedisTestCase.test_set_pocast
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

    def test_set_pocast(self):
        from sysk import Pocast
        p = Pocast('测试', 'wulala', 'www.baidu.com', None)
        res = SetNewPocast(p)
        self.assertTrue(res)


class MailTestCase(unittest.TestCase):
    def test_can_login(self):
        res = sendMail('测试', 'nihao')
        self.assertTrue(res)

    def test_can_sendfile(self):
        from mytoolkit import findAllFile
        for f in findAllFile():
            res = sendNewFile(f.FullPath)
            self.assertTrue(res)
            break


if __name__ == '__main__':
    unittest.main()
