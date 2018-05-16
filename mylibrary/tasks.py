from __future__ import absolute_import, unicode_literals
from celery import Celery, task, shared_task

from time import ctime

import mytoolkit
import sysk


@shared_task
def test_celery(x, y):
    print('hello ' + ctime())
    return x + y


@shared_task
def downloadSysk():
    print('check sysk')
    downloadpath = mytoolkit.getDownloadPath()
    print('download path: '+downloadpath)
    feeds = sysk.fetchRss('https://feeds.megaphone.fm/stuffyoushouldknow')
    #feeds = fetchRss('http://www.ximalaya.com/album/269179.xml')
    print("recive %s pocasts" % (len(feeds)))
    newfeeds = sysk.whichNew(feeds, downloadpath)
    newfeedsLen = len(newfeeds)
    print("found %s new pocasts" % (newfeedsLen))
    res = []
    for f in newfeeds:
        if sysk.downloadSksy(f, downloadpath):
            res.append(f.Title)
    print(str(res))
    return res
