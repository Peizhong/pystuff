# Create your tasks here
from __future__ import absolute_import, unicode_literals
# @shared_task decorator lets you create tasks without having any concrete app instance
from celery import shared_task
from celery.utils.log import get_task_logger

import os
import logging
import time

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from .models import Podcast

from myutils import query_config, replace_invalid_filename_char
from myutils.sysk import fetchRss, downloadOnePocastUsingAria2

MAX_AUTO_DOWNLOAD = 3
DOWNLOAD_PATH = query_config('path').get('sysk')
ADVERTISING = '<br><br>Learn more'

# todo add log to elk
logger = logging.getLogger("pystuff")

extra = {
    'x_app': "python",
    "x_module":"worker"
}

logger.info("hello",extra=extra)

# should not depend on the project

@shared_task
def scanDownloadPath():
    logger.info("scan local path")
    def file_exists(title: str):
        encodedName = replace_invalid_filename_char(title)
        filepath = '%s/%s.mp3' % (DOWNLOAD_PATH, encodedName)
        if os.path.exists(filepath):
            return filepath
        return None

    for p in Podcast.objects.all():
        # 检查是否存在
        path = file_exists(p.Title)
        if path:
            p.Status = 3
            p.Location = path
        # 已经下载过，又删除了
        elif p.Status == 3:
            p.Status = 5
        p.save()

@shared_task
def updatePodcastList():
    logger.info("update podcast list start")
    # 获取最近的列表
    fetchPodcasts = fetchRss('https://feeds.megaphone.fm/stuffyoushouldknow')
    logger.info("found %d new podcasts",len(fetchPodcasts))
    marked_count = 0
    for p in fetchPodcasts:
        willDownload = 'SYSK Selects' in p.Title and marked_count < MAX_AUTO_DOWNLOAD
        if willDownload:
            marked_count+=1
        obj, created = Podcast.objects.update_or_create(
            Title=p.Title,
            defaults={
                'Summary': p.Summary, # if (ADVERTISING not in p.Summary) else (p.Summary[:(p.Summary.index(ADVERTISING))]),
                'Link': p.Link,
                'PublishDate': p.PublishDate,
                # 筛选sysk select 的数据，标记下载
                'Status': 1 if willDownload else 0
            }
        )
    logger.info("update podcast's database completed")
    scanDownloadPath()
    return "complete"

@shared_task
def downloadNewPodcast():
    # todo: aria2 to speed up
    logger.info("start downloading")
    #重新下载已标记和错误的文件
    todownloads = Podcast.objects.filter(Q(Status=1) | Q(Status=4))
    print('%d to do' % todownloads.count())
    for todo in todownloads:
        todo.Status = 2
        todo.save()
        try:
            downloadedpath = downloadOnePocastUsingAria2(todo, DOWNLOAD_PATH) 
            todo.Location = downloadedpath
            todo.Remark = None
            todo.Status = 3
        except Exception as e:
            todo.Status = 4
            todo.Remark = repr(e)
        todo.save()
    return 'ok'