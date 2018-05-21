from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template import loader
from urllib import parse
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
    context = {
        'documents': mytoolkit.findAllDownloadFile(),
        'logs': mytoolkit.findAllFile('logs'),
        'form': form,
    }
    return render(request, 'mylibrary/index.html', context)


def downloadLog(request, fid):
    f = mytoolkit.getFileInfo(fid)
    with open(f.FullPath) as fl:
        c = fl.read()
    return HttpResponse(c)


def player(request, fid):
    f = mytoolkit.getDownloadFileInfo(fid)
    context = {
        'fileUrl': parse.quote(f.UrlPath)
    }
    return render(request, 'mylibrary/player.html', context)
