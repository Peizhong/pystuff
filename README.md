# py

hello

# cmd

docker exec -it 3e6 bash
celery -A learning_log worker -B -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

# todo
server:
	2。 收到用户id，查找对应的本地目录，更新hash值到redis
	3. 返回文件路径、时间戳、hash值
client:
	1. 发起链接，提供用户id
	4. 返回的数据与本地数据比对，hash值不一致的取时间最新的
