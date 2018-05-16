import platform
import time
import feedparser
import os
import socket
import collections
from atexit import register
from time import sleep, ctime
import sys
from urllib import request
import logging

LOG_FORMAT = "%(asctime)s - %(levelname)s - :%(lineno)d - %(message)s"
DATE_FORMAT = "%m-%d-%Y %H:%M:%S"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT,
                    filename="logs/sksy.log")


Pocast = collections.namedtuple(
    'Pocast', ['Title', 'Summary', 'Link', 'UpdateTime'])


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
    return feeds[:3]


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


def whichNew(feeds, localpath):
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


def downloadSksy(rss, localpath):
    result = False
    try:
        encode = replace_invalid_filename_char(rss.Title)
        filepath = '%s/%s.mp3' % (localpath, encode)
        logging.info("start download from %s" % (rss.Link))
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36'
        }
        req = request.Request(rss.Link, headers=header)
        page = request.urlopen(req)
        data = page.read()
        with open(filepath, "wb") as code:
            code.write(data)
        result = True
        # todo 数据库记录
    except Exception as e:
        print(e)
        result = False
    finally:
        return result


def syskTask(downloadPath):
    "给定时任务用的，不用考虑什么时候下载"
    logging.info('start sysk task')
    feeds = fetchRss('https://feeds.megaphone.fm/stuffyoushouldknow')
    print("recive %r pocasts" % len(feeds))
    newfeeds = whichNew(feeds, downloadPath)
    newfeedsLen = len(newfeeds)
    print("found %r new pocasts" % newfeedsLen)
    if newfeedsLen < 1:
        return
    downloadAll = [downloadSksy(nf, downloadPath) for nf in newfeeds]
    logging.info('sksy task completed')


def startSysk(downloadpath, autodown=True, hour=0):
    if(autodown):
        print("auto download pocast at %02d:00 " % (hour))
        lastcheckDate = -1
        while True:
            localtime = time.localtime(time.time())
            print("run job at %02d:%02d" %
                  (localtime.tm_hour, localtime.tm_min))
            # 每天只下载一次
            if(localtime.tm_yday == lastcheckDate):
                print('%s job is finished' % (time.asctime(localtime)))
                time.sleep(3600)
                continue
            # 除了第一次，每天只在指定的时间下载文件，过了就不管
            if (lastcheckDate == -1 or localtime.tm_hour == hour):
                print('time to check new pocast')
                # feeds = fetchRss('http://www.ifanr.com/feed')
                feeds = fetchRss(
                    'https://feeds.megaphone.fm/stuffyoushouldknow')
                # feeds = fetchRss('http://www.ximalaya.com/album/269179.xml')
                print("recive %s pocasts" % (len(feeds)))
                newfeeds = whichNew(feeds, downloadpath)
                newfeedsLen = len(newfeeds)
                print("found %s new pocasts" % (newfeedsLen))
                if(newfeedsLen == 0):
                    lastcheckDate = localtime.tm_yday
                    continue
                allLoaded = True
                for nf in newfeeds:
                    allLoaded = allLoaded and downloadSksy(nf, downloadpath)
                if(allLoaded == True):
                    lastcheckDate = localtime.tm_yday
                    continue
                if(allLoaded == False):
                    time.sleep(300)
            else:
                time.sleep(600)
    else:
        print('hello, fetching new pocasts....')
        feeds = fetchRss('http://www.ifanr.com/feed')
        # feeds = fetchRss('https://feeds.megaphone.fm/stuffyoushouldknow')
        print("recive %s pocasts" % (len(feeds)))
        newfeeds = whichNew(feeds, downloadpath)
        newfeedsLen = len(newfeeds)
        print("found %s new pocasts" % (newfeedsLen))
        index = 0
        for nf in newfeeds:
            index += 1
            print("%2d %s" % (index, nf['Title']))
        while True:
            inStr = input('select the number you want to download: ')
            try:
                indexToDownload = int(inStr)
                if (indexToDownload > 0 and indexToDownload <= newfeedsLen):
                    todo = newfeeds[indexToDownload-1]
                    downloadSksy(todo, downloadpath)
                    break
                else:
                    print('input number error')
            except:
                print('input value error')


def _main():
    curOs = platform.system()
    print('current os is '+curOs)
    curRealse = platform.release()
    print('current release is '+curRealse)
    if curOs == "Darwin":
        downloadpath = r'/Users/Peizhong/Downloads'
    elif curOs == "Linux":
        hostname = socket.gethostname()
        if 'raspberry' in hostname:
            downloadpath = r'/home/pi/downloads'
        else:
            downloadpath = r'/home/peizhong/downloads'
    else:
        downloadpath = r'E:/Downloads'
    syskTask(downloadpath)
    # startSysk(autodown=False, hour=1, downloadpath=downloadpath)


if __name__ == '__main__':
    _main()


@register
def _atexit():
    # 脚本退出前执行这个函数
    print('script end at '+ctime())
