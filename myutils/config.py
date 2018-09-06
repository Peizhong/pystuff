config = {
    'hosts':['localhost',],
    'celery_broker': 'amqp://localhost:5672',
    'celery_backend': 'django-db',
    'database_sqlite': {
        'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'database_mysql': {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "pystuff",
        "USER": "root",
        "PASSWORD": "mypass",
        "HOST": "localhost",
        "PORT": "3306"
    }
}
