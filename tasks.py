from celery import Celery

app = Celery('tasks', broker='redis://193.112.41.28:6379/0')


@app.task
def add(x, y):
    return x + y
