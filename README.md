# py

hello

# cmd

docker exec -it 3e6 bash
celery -A learning_log worker -B -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
