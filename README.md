# py

hello

 celery -A pystuff worker --pool=solo -l info
 celery -A pystuff beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler