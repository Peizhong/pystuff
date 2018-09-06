config = {
    'celery_broker': 'amqp://rabbit:5672',
    'celery_backend': 'amqp://rabbit:5672',
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
