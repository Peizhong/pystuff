from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from .models import Topic, Entry


def index(request):
    topicList = Topic.objects.order_by('date_add')[:5]
    topicOutput = ', '.join([t.topic for t in topicList])
    print('topic: '+topicOutput)
    entryList = Entry.objects.order_by('-date_add')[:5]
    entryOutput = ', '.join([e.title for e in entryList])
    print('entry: '+entryOutput)
    context = {
        'topicList': topicList,
        'entryList': entryList
    }
    return render(request, 'learning_logs/index.html', context)


def entry(request, entry_id):
    obj = get_object_or_404(Entry, pk=entry_id)
    return render(request, 'learning_logs/entry.html', {'entry': obj})


def topic(request, topic_id):
    t = get_object_or_404(Topic, pk=topic_id)
    e = t.entry_set.order_by('-date_add')
    return render(request, 'learning_logs/topic.html', {'topic': t, 'entryList': e})
