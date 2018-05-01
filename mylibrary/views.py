from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.template import loader

from . import filehelper


def index(request):
    context = {
        'files': filehelper.findAllFile(),
    }
    return render(request, 'mylibrary/index.html', context)


def player(request, file_name):
    context = {
        'file_server': 'http://192.168.3.172/downloads/',
        'file_name': file_name
    }
    return render(request, 'mylibrary/player.html', context)
