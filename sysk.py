import platform
import time
import feedparser
import os
import urllib.request


def fetchRss(rss):
    source = feedparser.parse(rss)
    feeds = [{'Title': e.title, 'UpdateTime': e.updated,
              'Summary': e.summary, 'Link': e.link} for e in source.entries]
    #byd = sorted(feeds, key=lambda s: s['UpdateTime'], reverse=True)
    # return byd[:5]
    return feeds[:5]


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
            if(f.find(rs['Title']) >= 0):
                ex = True
                break
        if(ex == False):
            newpocast.append(rs)

    return newpocast


def downloadSksy(rss, localpath):
    result = False
    try:
        filepath = '%s/%s.mp3' % (localpath, rss['Title'])
        print("start download to %s" % (filepath))
        f = urllib.request.urlopen(rss['Link'])
        data = f.read()
        with open(filepath, "wb") as code:
            code.write(data)
        result = True
    except:
        result = False
    finally:
        return result


def main(downloadpath, autodown=True, hour=0):
    if(autodown):
        print("auto download pocast at %02d:00 " % (hour))
        lastcheckDate = -1
        while True:
            localtime = time.localtime(time.time())
            # 每天只下载一次
            if(localtime.tm_yday == lastcheckDate):
                print('%s job is finished' % (time.asctime(localtime)))
                time.sleep(3600)
                continue
            # 每天只在指定的时间下载文件，过了就不管
            if (localtime.tm_hour == hour):
                print('time to download new pocast')
                #feeds = fetchRss('http://www.ifanr.com/feed')
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
        #feeds = fetchRss('https://feeds.megaphone.fm/stuffyoushouldknow')
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
                if (indexToDownload < newfeedsLen):
                    todo = newfeeds[indexToDownload]
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
    downloadpath = r'/Users/Peizhong/Downloads/'
else:
    downloadpath = r'E:/Downloads/'
main(autodown=True, hour=17, downloadpath=downloadpath)
