from django.urls import path

from . import views

app_name = 'podcasts'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('podcasts/<int:page>/', views.podcasts, name='podcasts'),
    path('whatsup', views.whatsup, name='whatsup'),
    path('downloaded', views.downloaded, name='downloaded')
]
