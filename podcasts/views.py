from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from .models import Podcast
import redis
import json
import time
import myutils
import myutils.sysk


pagesize = 20


def podcasts(request, page=0):
    redis_config = myutils.query_config('redis_connection')
    conn = redis.Redis(host=redis_config['host'], port=6379,
                       password=redis_config['password'], decode_responses=True)
    ps = {}
    ps['length'] = conn.llen('podcasts')
    ls = conn.lrange('podcasts', page*pagesize, (page+1)*pagesize)
    dt = []
    for p in ls:
        j = json.loads(p)
        dt.append(j)
        # dt.append(myutils.sysk.Podcast(p['Title'],p['Summary'],p['Link'],p['PublishDate'],p['DownloadResult']))
    ps['items'] = dt
    return HttpResponse(json.dumps(ps), content_type='application/json', status=200)


def whatsup(request):
    latest_podcasts_list = Podcast.objects.order_by('-PublishDate')[:10]
    context = {
        'latest_podcasts_list': latest_podcasts_list,
    }
    return render(request, 'podcasts/index.html', context)


class IndexView(generic.ListView):
    template_name = 'podcasts/index.html'
    context_object_name = 'latest_podcasts_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Podcast.objects.order_by('-PublishDate')[:10]


def downloaded(request):
    return HttpResponse("these ara downloaded files")
