# posts/urls.py
from django.urls import path
from .views import all_post, insert_post, post_detail, like_post, add_comment,get_data

urlpatterns = [
    path('', all_post, name='all_post'),
    path('insert_post/', insert_post, name='insert_post'),
    path('get_data/<int:post_id>/', get_data, name='get_data'),
    path('post_detail/<int:post_id>/', post_detail, name='post_detail'),
    path('like_post/<int:post_id>/<int:like_id>', like_post, name='like_post'),
    path('add_comment/<int:post_id>/', add_comment, name='add_comment'),
]
