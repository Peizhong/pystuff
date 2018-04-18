import platform
import time
import feedparser
import os
import sys
import urllib.request


def fetchRss(rss):
    source = feedparser.parse(rss)
    feeds = [{'Title': e.title, 'UpdateTime': e.updated,
              'Summary': e.summary, 'Link': e.link} for e in source.entries]
    # byd = sorted(feeds, key=lambda s: s['UpdateTime'], reverse=True)
    # return byd[:5]
    return feeds[:5]


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
    for root, dirs, files in os.walk(localpath):
        for name in files:
            if(name[-4:].lower() == '.mp3'):
                exfile.append(name)
        break
    for rs in feeds:
        ex = False
        for f in exfile:
            if(f.find(replace_invalid_filename_char(rs['Title'])) >= 0):
                ex = True
                break
        if(ex == False):
            newpocast.append(rs)

    return newpocast


def downloadSksy(rss, localpath):
    result = False
    try:
        encode = replace_invalid_filename_char(rss['Title'])
        filepath = '%s/%s.mp3' % (localpath, encode)
        print("start download to %s" % (filepath))
        f = urllib.request.urlopen(rss['Link'])
        data = f.read()
        with open(filepath, "wb") as code:
            code.write(data)
        result = True
    except Exception as e:
        print(e)
        result = False
    finally:
        return result


def main(downloadpath, autodown=True, hour=0):
    if(autodown):
        print("auto download pocast at %02d:00 " % (hour))
        lastcheckDate = -1
        while True:
            localtime = time.localtime(time.time())
            print("check pocast at %02d:%02d" %
                  (localtime.tm_hour, localtime.tm_min))
            # 每天只下载一次
            if(localtime.tm_yday == lastcheckDate):
                print('%s job is finished' % (time.asctime(localtime)))
                time.sleep(3600)
                continue
            # 每天只在指定的时间下载文件，过了就不管
            if (localtime.tm_hour == hour):
                print('time to download new pocast')
                # feeds = fetchRss('http://www.ifanr.com/feed')
                feeds = fetchRss(
                    'https://feeds.megaphone.fm/stuffyoushouldknow')
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


curOs = platform.system()
print('current os is '+curOs)
curRealse = platform.release()
print('current release is '+curRealse)
if curOs == "Darwin":
    downloadpath = r'/Users/Peizhong/Downloads'
elif curOs == "Linux":
    downloadpath = r'/home/Peizhong/Downloads'
else:
    downloadpath = r'E:/Downloads'

main(autodown=True, hour=10, downloadpath=downloadpath)
