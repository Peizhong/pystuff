from django.urls import path
from django.conf.urls import url

from . import views

app_name = 'learning_logs'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    path('entry/<str:entry_id>/', views.entry, name='entry'),
    path('new_entry/<str:topic_id>/', views.new_entry, name='new_entry'),
    path('topic/<str:topic_id>/', views.topic, name='topic'),
    path('new_entry/', views.new_topic, name='new_topic'),
]
