import sys
import requests

url = r'http://193.112.41.28:8000/users/login/'

client = requests.session()

client.get(url)

if 'csrftoken' in client.cookies:
    csrftoken = client.cookies['csrftoken']

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
}
# https://www.cnblogs.com/whatbeg/p/5320666.html
login_data = dict(username='admin', password='hello123',
                  csrfmiddlewaretoken=csrftoken, next='/')
r = client.post(url, data=login_data, headers=dict(Referer=url))
r = client.get(r'http://193.112.41.28:8000/learning_logs/', headers=header)
