config = {
    'hosts': ['localhost', '192.168.1.100', '192.168.1.108'],
    'file_server': 'http://192.168.1.100/',
    'path': {
        'log': 'log',
        'sysk': 'downloads/sysk/'
    },
    'celery_broker': 'pyamqp://192.168.1.108//',
    'celery_backend': 'django-db',
    'redis_connection': {
        'host': 'redis',
        'password': 'password'
    }
}
