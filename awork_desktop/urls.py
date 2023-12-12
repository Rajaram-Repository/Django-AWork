from django.urls import path
from . import views

urlpatterns = [
    path('api/set-hash',views.hash,name='set-hash'),
    path('',views.desktop,name='mydesktop'),
]