import unittest
import urllib.request
'''
python -m unittest foo.tests.MailTestCase
python -m unittest foo.tests.RedisTestCase.test_set_pocast
'''

import logging

logger = logging.getLogger(__name__)


class MailTestCase(unittest.TestCase):
    def test_can_sendfile(self):
        ''''''
        from mytoolkit import findAllDownloadFile
        from foo.Mail import sendNewFile
        for id, _ in findAllDownloadFile().items():
            res = sendNewFile(id)
            self.assertTrue(res)
            break


class SyncTestCase(unittest.TestCase):
    test_account = 'test'
    test_password = 'hello123'

    def test_hello(self):
        pass

    def test_register(self):
        '''测试注册账号'''

    def test_login(self):
        '''验证用户名密码登陆'''
        login_url = r'http://193.112.41.28:8000/users/login/'
        data = {"username": self.test_account, "password": self.test_password}
        post_data = urllib.parse.urlencode(data).encode('utf-8')
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        }
        req = urllib.request.Request(
            login_url, headers=headers)
        print(req)
        pass

    def test_setupsync(self):
        '''设置同步内容'''
        pass

    def test_getfilelist(self):
        '''登陆成功后，获取服务器文件信息'''
        pass

    def test_difffile(self):
        '''比较文件异常'''
        pass

    def test_updatefile(self):
        '''根据服务器信息'''
        pass


if __name__ == '__main__':
    unittest.main()
