from django.urls import path

from . import views

urlpatterns = [
        path('',views.index,name='awork'),

        path('signup',views.signup,name='signup'),
        path('signin',views.signin,name='signin'),
        
        path('home',views.home,name='home'),
        path('profile',views.profile,name='profile'),

        path('logout',views.user_logout,name='logout'),

        path('test',views.test,name='test'),
]