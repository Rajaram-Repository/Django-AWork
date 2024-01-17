from django.urls import path

from . import views

urlpatterns = [
        path('',views.index,name='awork'),

        path('signup',views.signup,name='signup'),
        path('signin',views.signin,name='signin'),

        path('api_auth',views.api_auth,name='api_auth'),

        path('send_otp',views.send_otp,name='send_otp'),
        path('verify_otp',views.verify_otp,name='verify_otp'),

        path('home',views.home,name='home'),
        path('profile',views.profile,name='profile'),

        path('logout',views.user_logout,name='logout'),

        path('test',views.test,name='test'),
]