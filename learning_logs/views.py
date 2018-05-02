from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


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
    entry = get_object_or_404(Entry, pk=entry_id)
    topic = entry.topic
    if request.method != 'POST':
        form = EntryForm(instance=entry)
    else:
        # 处理POST提交的数据
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:index'))
    context = {'form': form, 'entry': entry,
               'topic': topic, 'error_message': 'hello'}
    return render(request, 'learning_logs/entry.html', context)


def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if request.method != 'POST':
        form = EntryForm(initial={'topic': topic})
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:index'))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


def topic(request, topic_id):
    t = get_object_or_404(Topic, pk=topic_id)
    e = t.entry_set.order_by('-date_add')
    return render(request, 'learning_logs/topic.html', {'topic': t, 'entryList': e})
