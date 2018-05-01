from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
    path('', views.index, name='index'),
    path('entry/<str:entry_id>/', views.entry, name='entry'),
    path('topic/<str:topic_id>/', views.topic, name='topic')
]
