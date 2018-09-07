import os
import sys
import feedparser
import collections
from atexit import register
from time import ctime
import requests

Pocast = collections.namedtuple(
    'Pocast', ['Title', 'Summary', 'Link', 'UpdateTime'])

DownloadResult = collections.namedtuple('DownloadResult',['Title', 'Url', 'Result'])


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
        feeds.append(Pocast(s.title, s.summary, link, s.updated))
    # byd = sorted(feeds, key=lambda s: s['UpdateTime'], reverse=True)
    # return byd[:5]
    return feeds[:100]


def replace_invalid_filename_char(filename, replaced_char='_'):
    '''Replace the invalid characaters in the filename with specified characater.
    The default replaced characater is '_'.
    e.g.
    C/C++ -> C_C++
    '''
    valid_filename = filename
    invalid_characaters = '\\/:*?"<>|'
    for c in invalid_characaters:
        # print 'c:', c
        valid_filename = valid_filename.replace(c, replaced_char)

    return valid_filename


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
    '''return file path'''
    result = ''
    try:
        encodedName = replace_invalid_filename_char(rss.Title)
        filepath = '%s/%s.mp3' % (localpath, encodedName)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        }
        print('downloading from: '+rss.Link)
        r = requests.get(rss.Link,headers=headers, stream=True) # create HTTP response object
        with open(filepath,'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        result = filepath
        # todo 数据库记录
    except Exception as e:
        print(e)
        result = e
    finally:
        return result


def checkAndDownloadPocasts(url, downloadpath, maxcount=5):
    print('hello, fetching new pocasts....')
    if not os.path.exists(downloadpath):
        os.makedirs(downloadpath)
    feeds = fetchRss(url)
    print("recive %s pocasts" % (len(feeds)))
    newfeeds = whatsNew(feeds, downloadpath)
    newfeedsLen = len(newfeeds)
    print("found %s new pocasts" % (newfeedsLen))
    result = []
    while maxcount > 0:
        maxcount = maxcount-1
        todo = newfeeds[maxcount]
        res = downloadOnePocast(todo, downloadpath)
        result.append(DownloadResult(todo.Title,todo.Link,res))
    return result


def main():
    url = 'https://feeds.megaphone.fm/stuffyoushouldknow'
    checkAndDownloadPocasts(url, 'downloads/sysk')


if(__name__ == '__main__'):
    main()


@register
def _atexit():
    # 脚本退出前执行这个函数
    print('sysk srcript end at ' + ctime())
