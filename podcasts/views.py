from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic
from django.db.models import Q

from .models import Podcast
from .tasks import updateFileInfo

updateFileInfo()

class IndexView(generic.ListView):
    template_name = 'podcasts/index.html'
    context_object_name = 'latest_podcasts_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Podcast.objects.order_by('-PublishDate')[:100]
        
    def post(self, request):
        try:
            data = request.POST['ids']
            ids = data.split(',')
            Podcast.objects.filter(pk__in=ids).filter(~Q(Status=3)).update(Status=1)
            return HttpResponse("ok")
        except Exception:
            return HttpResponse("error")

class DownloadedView(generic.ListView):
    template_name = 'podcasts/downloaded.html'
    context_object_name = 'latest_podcasts_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Podcast.objects.filter(Status=3).order_by('-PublishDate')[:100]

