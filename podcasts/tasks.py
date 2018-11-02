# Create your tasks here
from __future__ import absolute_import, unicode_literals
# @shared_task decorator lets you create tasks without having any concrete app instance
from celery import shared_task

from .models import Podcast

import time
from myutils.sysk import checkAndDownloadPodcasts


@shared_task
def downloadPocasts(*args):
    if args:
        strArgs = ','.join(repr(s) for s in args)
        print('start download pocasts with args %r at %r' %
              (strArgs, time.ctime()))
    else:
        print('start download pocasts at %r' % time.ctime())
    result = checkAndDownloadPodcasts(
        'https://feeds.megaphone.fm/stuffyoushouldknow', 'downloads/sysk')
    print('download pocasts result: %r' % result)
    return result


@shared_task
def sayhi():
    what = Podcast.objects.order_by('-PublishDate')[:10]
    s = ','.join(p.Title for p in what)
    print(s)
