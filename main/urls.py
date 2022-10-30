from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    re_path(r'^login/$', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
]