from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm

import logging

logger = logging.getLogger(__name__)


@login_required
def index(request):
    logger.warn('get learing index')
    topicList = Topic.objects.filter(owner=request.user).order_by('date_add')
    # topicList = Topic.objects.order_by('date_add')
    entryList = []
    for topic in topicList:
        for e in topic.entry_set.order_by('-date_add'):
            entryList.append(e)
    context = {
        'topicList': topicList,
        'entryList': entryList
    }
    return render(request, 'learning_logs/index.html', context)


@login_required
def entry(request, entry_id):
    entry = get_object_or_404(Entry, pk=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
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


@login_required
def new_entry(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        form = EntryForm(initial={'topic': topic})
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            form.save()
            # todo: 跳转到当前主题
            return HttpResponseRedirect(reverse('learning_logs:topic', args=(topic_id,)))
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def topic(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    if topic.owner != request.user:
        raise Http404
    entry = topic.entry_set.order_by('-date_add')
    return render(request, 'learning_logs/topic.html', {'topic': topic, 'entryList': entry})


@login_required
def new_topic(request):
    if request.method != 'POST':
        form = TopicForm()
    else:
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:index'))
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)
