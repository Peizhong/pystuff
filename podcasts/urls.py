from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('podcasts/<int:page>/', views.podcasts, name='podcasts'),
]