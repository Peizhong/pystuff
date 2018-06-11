from django.test import TestCase

# Create your tests here.


class SyskTests(TestCase):
    def test_connect_pocast(self):
        ''''''
        from sysk import fetchRss
        feeds = fetchRss('https://feeds.megaphone.fm/stuffyoushouldknow')
        self.assertIs(len(feeds) > 0, True)

    def test_send_new_mail(self):
        from mytoolkit import findAllDownloadFile
        from foo.Mail import sendNewFile
        for _, info in findAllDownloadFile().items():
            # 测试发送一封邮件
            self.assertIs(sendNewFile(info.FullPath), True)
            return


class SyncTests(TestCase):
    def test_can_login(self):
        from foo.NetClient import NetClient
        client = NetClient('http://193.112.41.28:8000', 'admin', 'hello123')
        self.assertTrue(client.login('users/login/'))
        self.assertTrue(client.GetData('mylibrary/'))
