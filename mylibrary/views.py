from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template import loader
import os
from .models import Document
from .forms import DocumentForm
import logging

import mytoolkit

logger = logging.getLogger(__name__)


@login_required
def index(request):
    logger.warn('get mylibrary index')
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile=request.FILES['docfile'])
            newdoc.owner = request.user
            newdoc.save()
            return HttpResponseRedirect(reverse('mylibrary:index'))
    else:
        form = DocumentForm()
    documents = Document.objects.filter(
        owner=request.user).order_by('date_add')
    files = []
    for d in documents:
        [dirname, filename] = os.path.split(d.docfile.path)
        files.append(filename)
    context = {
        'documents': mytoolkit.findAllFile(),
        'form': form,
    }
    return render(request, 'mylibrary/index.html', context)


def player(request, file_name):
    file_url = ''
    for f in mytoolkit.findAllFile():
        if f.Name == file_name:
            file_url = f.UrlPath
    context = {
        'fileUrl': file_url
    }
    return render(request, 'mylibrary/player.html', context)
