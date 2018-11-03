import os
import sys
import feedparser
import collections
from atexit import register
import time
import requests
import json

from myutils import query_config, replace_invalid_filename_char


class Podcast:
    def __init__(self,title,summary,link,publishdate,downloadresult):
        self.Title = title
        self.Summary = summary
        self.Link = link
        self.PublishDate = time.strftime("%Y-%m-%d %H:%M:%S",publishdate)
        self.DownloadResult = downloadresult

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

def fetchRss(rss):
    feeds = []
    source = feedparser.parse(rss)
    for s in source.entries:
        link = ''
        for l in s.links:
            if (l['type'] == 'audio/mpeg'):
                link = l['href']
                break
        if not link:
            continue
        #feeds.append(Pocast(s.title, s.subtitle, link, time.strftime("%Y-%m-%d %H:%M:%S",s.published_parsed,''))
        feeds.append(Podcast(s.title, s.summary, link,s.published_parsed,''))
    # byd = sorted(feeds, key=lambda s: s['UpdateTime'], reverse=True)
    # return byd[:5]
    return feeds[:100]


def whatsNew(feeds, localpath):
    newpocast = []
    exfile = []
    # 拆包，没有用的元素用_代替
    for _, _, files in os.walk(localpath):
        for name in files:
            if '.' not in name:
                continue
            if os.path.splitext(name)[1] == '.mp3':
                exfile.append(name)
        break
    for rs in feeds:
        ex = False
        for f in exfile:
            if(f.find(replace_invalid_filename_char(rs.Title)) >= 0):
                ex = True
                break
        if(ex == False):
            newpocast.append(rs)

    return newpocast


def downloadOnePocast(rss, localpath):
    '''return file path, may excepetion'''
    result = ''
    encodedName = replace_invalid_filename_char(rss.Title)
    filepath = '%s/%s.mp3' % (localpath, encodedName)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
    }
    print('downloading from: '+rss.Link)
    r = requests.get(rss.Link,headers=headers, stream=True) # create HTTP response object
    with open(filepath,'wb') as f:
        for chunk in r.iter_content(chunk_size=4096):
             if chunk:
                f.write(chunk)
    result = filepath
    return result

'''
def updateLocalPocastList(podcasts:list, downloadpath:str):
    for p in podcasts:
        if p.DownloadResult:
            continue
        encodedName = replace_invalid_filename_char(p.Title)
        filepath = '%s/%s.mp3' % (downloadpath, encodedName)
        if os.path.exists(filepath):
            p.DownloadResult = filepath
    redis_config = query_config('redis_connection')
    conn = redis.Redis(host=redis_config['host'],port=6379,password=redis_config['password'],decode_responses=True)
    conn.delete('podcasts')
    pipe = conn.pipeline()
    for p in podcasts:
        pipe.rpush('podcasts',p.toJSON())
    pipe.execute()
'''

def checkAndDownloadPodcasts(url, downloadpath, maxcount=1):
    print('hello, fetching new podcasts....')
    if not os.path.exists(downloadpath):
        os.makedirs(downloadpath)
    podcasts = fetchRss(url)
    #updateLocalPocastList(podcasts, downloadpath)
    print("recive %s podcasts" % (len(podcasts)))
    newfeeds = whatsNew(podcasts, downloadpath)
    newfeedsLen = len(newfeeds)
    print("found %s new podcasts" % (newfeedsLen))
    downloadResult = []
    while maxcount > 0:
        maxcount = maxcount-1
        todo = newfeeds[maxcount]
        oneResult = downloadOnePocast(todo, downloadpath)
        downloadResult.append((todo.Title,todo.Link,oneResult))
    #updateLocalPocastList(podcasts, downloadpath)
    return downloadResult


def main():
    url = 'https://feeds.megaphone.fm/stuffyoushouldknow'
    checkAndDownloadPodcasts(url, 'downloads/sysk')


if(__name__ == '__main__'):
    main()


@register
def _atexit():
    # 脚本退出前执行这个函数
    print('sysk srcript end at ' + time.ctime())
