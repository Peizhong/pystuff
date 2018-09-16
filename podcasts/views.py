from django.http import HttpResponse
import redis
import json
import time
import myutils
import myutils.sysk

def index(request):
    return HttpResponse("Hello, world. You're at the podcasts index.")


pagesize=20
def podcasts(request,page=0):
    redis_config = myutils.query_config('redis_connection')
    conn = redis.Redis(host=redis_config['host'],port=6379,password=redis_config['password'],decode_responses=True)
    ps = {}
    ps['length']=conn.llen('podcasts')
    ls = conn.lrange('podcasts',page*pagesize,(page+1)*pagesize)
    dt = []
    for p in ls:
        j = json.loads(p)
        dt.append(j)
        #dt.append(myutils.sysk.Podcast(p['Title'],p['Summary'],p['Link'],p['PublishDate'],p['DownloadResult']))
    ps['items']=dt
    return HttpResponse(json.dumps(ps),content_type='application/json',status=200)