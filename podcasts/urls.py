from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'podcasts'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('index', views.IndexView.as_view(), name='index'),
    path('downloaded', views.DownloadedView.as_view(), name='downloaded'),
    path('test', views.TestView.as_view(), name='test'),
    url('delete', views.delete, name='delete'),
]
