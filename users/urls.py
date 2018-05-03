from django.conf.urls import url
from django.contrib.auth.views import login

from . import views

app_name = 'users'
urlpatterns = [
    # 登录页面
    url('login/', login, {'template_name': 'users/login.html'}, name='login'),
    url('logout/', views.logout_view, name='logout'),
    url('register/', views.register, name='register'),
]
