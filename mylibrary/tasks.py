from __future__ import absolute_import, unicode_literals
from celery import Celery, task, shared_task

import logging

import mytoolkit
import sysk

LOG_FORMAT = "%(asctime)s - %(levelname)s - :%(lineno)d - %(message)s"
DATE_FORMAT = "%m-%d-%Y %H:%M:%S"
logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT, datefmt=DATE_FORMAT,
                    filename="../logs/mytask.log")


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
    logging.warn('check sysk')
    downloadpath = mytoolkit.getDownloadPath()
    feeds = sysk.fetchRss('https://feeds.megaphone.fm/stuffyoushouldknow')
    #feeds = fetchRss('http://www.ximalaya.com/album/269179.xml')
    logging.warn("recive %s pocasts" % (len(feeds)))
    newfeeds = sysk.whichNew(feeds, downloadpath)
    newfeedsLen = len(newfeeds)
    logging.warn("found %s new pocasts" % (newfeedsLen))
    res = []
    for f in newfeeds:
        if sysk.downloadSksy(f, downloadpath):
            res.append(f.Title)
    logging.warn(str(res))


downloadSysk()
