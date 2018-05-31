from __future__ import absolute_import, unicode_literals
from celery import Celery, task, shared_task

from time import ctime

import logging

from foo.Mail import sendNewFile

import mytoolkit
import sysk

logger = logging.getLogger(__name__)


@shared_task
def downloadSysk():
    logger.info('check sysk')
    downloadpath = mytoolkit.getDownloadPath('sysk')
    logger.info('download path is ' + downloadpath)
    logger.info('now checking rss...')
    feeds = sysk.fetchRss('https://feeds.megaphone.fm/stuffyoushouldknow')
    #feeds = fetchRss('http://www.ximalaya.com/album/269179.xml')
    newfeeds = sysk.whichNew(feeds, downloadpath)
    newfeedsLen = len(newfeeds)
    logger.info("found %s new pocasts" % (newfeedsLen))
    res = []
    for f in newfeeds:
        npath = sysk.downloadSksy(f, downloadpath)
        if npath:
            res.append(npath)
            sendNewFile(npath)
    logger.info('downloaded: %s' % str(npath))
    return res
