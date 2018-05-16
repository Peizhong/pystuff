from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

import mytoolkit

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learning_log.settings')

host = mytoolkit.queryConfig('host')

app = Celery('learning_log', broker='redis://%s:6379' % host,
             backend='redis://%s:6379' % host)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


'''
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    sender.add_periodic_task(
        crontab(hour=7, minute=30, day_of_week=1),
        test.s('Happy Mondays!'),
    )
'''

app.conf.beat_schedule = {
    'every-day-check-pocast': {
        'task': 'mylibrary.tasks.downloadSysk',
        # every hour at midnight
        'schedule': crontab(minute=0, hour=0),
        # 'args': (16, 16)
    },
    'staying_alive': {
        'task': 'mylibrary.tasks.test_celery',
        'schedule': crontab(minute=1),
        'args': (4, 3)
    }
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task
def test(arg):
    print(arg)
