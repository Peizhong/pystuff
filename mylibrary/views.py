from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template import loader
import os
from .models import Document
from .forms import DocumentForm
from urllib import parse
import collections

import mytoolkit
from . import tasks


FileInfo = collections.namedtuple('FileInfo', ['Name', 'UrlPath'])


@login_required
def index(request):
    # res = tasks.add.delay(4, 3)
    # print('call celery:')
    # print(res.ready())
    # handle file upload
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
    packedfiles = []
    fileServer = mytoolkit.getFileServer()
    for f in mytoolkit.findAllFile():
        packedfiles.append(FileInfo(f, parse.quote(fileServer+f)))
    context = {
        'documents': packedfiles,
        'form': form,
    }
    return render(request, 'mylibrary/index.html', context)


def player(request, file_name):
    context = {
        'fileUrl':   mytoolkit.getFileServer()+parse.quote(file_name)
    }
    return render(request, 'mylibrary/player.html', context)
