# Create your tasks here
from __future__ import absolute_import, unicode_literals
# @shared_task decorator lets you create tasks without having any concrete app instance
from celery import shared_task

import time

@shared_task
def downloadPocasts(*args):
    if args:
        strArgs = ','.join(repr(s) for s in args)
        print('start download pocasts with args %r at %r'%(strArgs, time.ctime()))
    else:    
        print('start download pocasts at %r'%time.ctime())
    pass