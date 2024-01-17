from django.urls import path
from . import views

urlpatterns = [
    path('api/generate_token',views.generate_token,name='generate_token'),
    path('get_list', views.get_list, name='get_list'),
    path('all_messages', views.all_messages, name='all_messages'),

    path('get_all_list', views.get_all_list, name='get_all_list'),
    path('sync/<str:sync>/<str:flag>', views.desk_sync, name='desk_sync'),
    path('edit_schedule', views.edit_schedule, name='edit_schedule'),
    path('save_result', views.save_result, name='save_result'),

    path('api/set-hash',views.hash,name='set-hash'),
    path('api/is_valid_room',views.is_valid_room,name='is_valid_room'),
    path('api/verify_token',views.verify_token,name='verify_token'),
    path('',views.desktop,name='mydesktop'),
]