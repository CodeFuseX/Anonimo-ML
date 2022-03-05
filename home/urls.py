from typing import ValuesView
from django.http.request import validate_host
from django.urls import path,include
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.handlelogin, name='login'),
    path('signup/', views.signup, name='signup'),
    path('resources', views.resources, name='resources'),
    path('post',views.post, name='post'),
    path('logout/',views.handlelogout, name='logout'),
    path('settings',views.settings, name='settings'),
    path('edit/<int:id>',views.edit, name='edit'),
    path('complete',views.complete, name='update'),
    path('userprofile/<int:id>', views.userProfile, name="userprofile"),
    path('unfriend', views.unfriend, name="unfriend"),
    path('followers_count', views.followers_count, name='followers'),
    path('accept', views.accept_request, name='accept'),
    path('request', views.requestpage, name="request"),
    path('buycoins', views.buycoins, name="buycoins"),
    path('success/', views.success, name="success"),
    path('chatlist',views.chatlist, name = "chatlist"),



    


]

