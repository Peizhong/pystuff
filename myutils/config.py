config = {
    'hosts': ['localhost', 'http://192.168.1.100/'],
    'file_server': 'http://192.168.1.100/',
    'path': {
        'log': 'log',
        'sysk': 'downloads/sysk/'
    },
    'celery_broker': 'pyamqp://guest@192.168.1.108//',
    'celery_backend': 'django-db',
    'redis_connection': {
        'host': 'redis',
        'password': 'password'
    }
}
