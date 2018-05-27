from django.urls import path

from . import views

app_name = 'mylibrary'
urlpatterns = [
    path('', views.index, name='index'),
    path('player/<str:fid>/', views.player, name='player'),
    path('<str:fid>/', views.downloadLog, name='downloadLog'),
    path('upload', views.upload, name='upload')
]
