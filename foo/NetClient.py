import os
import sys
import requests


class NetClient():
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    }

    def __init__(self, rootUrl, account, password):
        self.Settings = {
            'ServiceUrl': rootUrl,
            'Account': account,
            'Password': password
        }
        self.Client = requests.session()

    def login(self, route):
        loginUrl = os.path.join(self.Settings['ServiceUrl'], route)
        response = self.Client.get(loginUrl)
        print(self.Client.cookies)
        if 'csrftoken' in self.Client.cookies:
            csrftoken = self.Client.cookies['csrftoken']
            login_data = {
                'username': self.Settings['Account'],
                'password': self.Settings['Password'],
                'csrfmiddlewaretoken': csrftoken,
                'next': '/mylibrary/'
            }
            response = self.Client.post(loginUrl, data=login_data,
                                        headers={'Referer': loginUrl})
            if response.reason == 'OK':
                return True
            return False

    def GetData(self, route, **params):
        if 'sessionid' not in self.Client.cookies:
            return None
        geturl = os.path.join(self.Settings['ServiceUrl'], route)
        response = self.Client.get(geturl, **params)
        if response.reason == 'OK':
            return response.text
        return None


if __name__ == '__main__':
    client = NetClient('http://193.112.41.28:8000', 'admin', 'hello123')
    if client.login('users/login/'):
        client.GetData('learning_loxgs')
