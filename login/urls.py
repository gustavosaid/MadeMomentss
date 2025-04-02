from django.urls import path
from login.views import (index, criar_user)

urlpatterns = [
    path('',index, name='index'),
    path('criar-user/',criar_user,name='criar_user')
]