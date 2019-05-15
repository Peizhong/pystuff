config = {
    'hosts': ['localhost', '193.112.41.28'],
    'file_server': 'http://193.112.41.28/',
    'path': {
        'log': 'log',
        'sysk': 'downloads/sysk/'
    },
    'celery_broker': 'pyamqp://193.112.41.28//',
    'celery_backend': 'django-db',
    'redis_connection': {
        'host': 'redis',
        'password': 'password'
    }
}
