from __future__ import absolute_import, unicode_literals
from celery import Celery, task, shared_task

import sysk
import mytoolkit


@shared_task
def add(x, y):
    print('hello tasks.add')
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@task
def test_celery(x, y):
    print(str(x + y))
    return x + y


@task
def downloadSysk():
    downloadpath = mytoolkit.getDownloadPath()
    feeds = sysk.fetchRss('https://feeds.megaphone.fm/stuffyoushouldknow')
    #feeds = fetchRss('http://www.ximalaya.com/album/269179.xml')
    print("recive %s pocasts" % (len(feeds)))
    newfeeds = sysk.whichNew(feeds, downloadpath)
    newfeedsLen = len(newfeeds)
    print("found %s new pocasts" % (newfeedsLen))
    return [f['Title'] for f in newfeeds]
