# py

# hello
python manage.py makemigrations podcasts
python manage.py migrate
python manage.py createsuperuser

celery -A pystuff worker --pool=solo -l info
celery -A pystuff beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler