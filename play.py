import redis
import json
import collections
import time

Pocast = collections.namedtuple(
    'Pocast', ['Title', 'Summary', 'Link', 'UpdateTime','FileLocation'])


ps = [Pocast(repr(p),'hello','link', time.localtime(), 'location') for p in range(1000)]


conn= redis.Redis(host='193.112.41.28',port=6379,password='9ol.)P:?',decode_responses=True)

ps = []
ls = conn.lrange('pocasts',1,10)
for l in ls:
    j = json.loads(l)
    p = Pocast(j[0],j[1],j[2],time.strftime("%Y-%m-%d %X",time.localtime(j[3])),j[4])
    ps.append(p)
    
#conn.delete('pocasts')
pipe = conn.pipeline()
for p in ps:
    pipe.hset('pocasts',p.Title,json.dumps(p))
pipe.execute()

f1to10 = conn.hgetall('pocasts')
for v in f1to10.values():
    p = json.loads(v)
