# py

hello

# cmd

docker exec -it 3e6 bash
celery -A learning_log worker -B -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler

# todo

server:
2。 收到用户 id，查找对应的本地目录，更新 hash 值到 redis 3. 返回文件路径、时间戳、hash 值
client: 1. 发起链接，提供用户 id 4. 返回的数据与本地数据比对，hash 值不一致的取时间最新的

#python
强类型、动态类型（编译时不检查、运行时检查类型)
多重继承
接口 abc.ABC
