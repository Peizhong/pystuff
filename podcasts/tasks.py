# Create your tasks here
from __future__ import absolute_import, unicode_literals
# @shared_task decorator lets you create tasks without having any concrete app instance
from celery import shared_task

import os
import time

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

from .models import Podcast

from myutils import query_config, replace_invalid_filename_char
from myutils.sysk import Podcast as rssPocast
from myutils.sysk import fetchRss, downloadOnePocast, checkAndDownloadPodcasts


MAX_AUTO_DOWNLOAD = 3
DOWNLOAD_PATH = query_config('path').get('sysk')
FILE_SERVER = query_config('file_server')
ADVERTISING = '<br><br>Learn more about advertising on the HowStuffWorks podcasts at'

#todo add log to elk

@shared_task
def updateFileInfo():
    def file_exists(title: str):
        encodedName = replace_invalid_filename_char(title)
        filepath = '%s/%s.mp3' % (DOWNLOAD_PATH, encodedName)
        if os.path.exists(filepath):
            return filepath
        return None

    # 查找所有标记了的文件，下载
    for p in Podcast.objects.all():
        # 检查是否存在
        path = file_exists(p.Title)
        if path:
            if p.Status != 4:
                p.Status = 3
                p.Location = path
                p.MirrorLink = os.path.join(FILE_SERVER, path)
        else:
            # 已经下载过，又删除了
            if p.Status == 3:
                p.Status = 5
        p.save()

@shared_task
def newDownloadPodcast():
    # 获取最近的列表
    fetchPodcasts = fetchRss('https://feeds.megaphone.fm/stuffyoushouldknow')
    # 写入数据库
    marked_count = 0
    for p in fetchPodcasts:
        obj, created = Podcast.objects.get_or_create(
            Title=p.Title,
            defaults={
                'Summary': p.Summary if (ADVERTISING not in p.Summary) else (p.Summary[:(p.Summary.index(ADVERTISING))]),
                'Link': p.Link,
                'PublishDate': p.PublishDate,
                # 筛选sysk select 的数据，标记下载
                'Status': 1 if ('SYSK Selects' in p.Title and marked_count < MAX_AUTO_DOWNLOAD) else 0
            }
        )
        if obj.Status == 1:
            marked_count += 1

    updateFileInfo()

    #重新下载已标记和错误的文件
    todownloads = Podcast.objects.filter(Q(Status=1) | Q(Status=4))
    for todo in todownloads:
        todo.Status = 2
        todo.save()
        try:
            downloadedpath = downloadOnePocast(todo, DOWNLOAD_PATH) 
            todo.Location = downloadedpath
            todo.MirrorLink = os.path.join(FILE_SERVER, downloadedpath)
            todo.Remark = None
            todo.Status = 3
        except Exception as e:
            todo.Status = 4
            todo.Remark = repr(e)
        todo.save()
    print('%d to do' % todownloads.count())
    return 'ok'
