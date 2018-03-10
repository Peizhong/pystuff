import feedparser
import requests
import urllib.request

from flask import Flask

app = Flask(__name__)

feed = feedparser.parse(
    'https://www.howstuffworks.com/podcasts/stuff-you-should-know.rss')
#feed = feedparser.parse('http://www.ifanr.com/feed')


def get_real_url(url):
    rs = requests.get(url)
    if rs.status_code > 400:
        return 'error'
    return rs.url


def downloadFile(info):
    print("downloading with urllib")
    f = urllib.request.urlopen(info[1])
    data = f.read()
    with open("downloads/"+info[0]+".mp3", "wb") as code:
        code.write(data)
    return 'okay'


if len(feed.entries) > 0:
    # 转换为元组
    feedList = [(e.title, e.link) for e in feed.entries]
    # 字典
    feedDict = [{f.title: f.link} for f in feed.entries]

    for f in feedList:
        al = downloadFile(f)
        break

print('hello, here is what i got')
