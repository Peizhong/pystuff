from django.urls import path

from . import views

app_name = 'podcasts'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('index', views.IndexView.as_view(), name='index'),
    path('downloaded', views.DownloadedView.as_view(), name='downloaded'),  
]
