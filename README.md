# py

hello

# cmd

docker exec -it 3e6 bash
celery -A learning_log worker -B -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

# what is this?

新闻聚合: 多账户(django), 订阅源(mysql), 采集文章(线程, 定时任务), 兴趣排序(redis), 加载文章(缓存)

# doto

0.  django 自带了那些功能
1.  编辑订阅源
1.  从订阅源爬数据到 Entry

1.
