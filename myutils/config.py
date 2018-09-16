config = {
    'hosts':['localhost',],
    'celery_broker': 'amqp://rabbit:5672',
    'celery_backend': 'django-db',
    'redis_connection':{
        'host':'redis',
        'password':'password'
    }
}
