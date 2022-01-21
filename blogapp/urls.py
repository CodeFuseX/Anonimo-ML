
from django.urls import path
from blogapp import views



urlpatterns = [
    path('/count/report',views.report, name='report' ),
    
    path('/count/badges',views.badges, name='badges' ),
    path('/postComment/comment', views.postComment, name="postComment"),
    path('', views.anonymhome, name='anonym'),
    path('like/', views.like_post, name='like-post'),
    path('/<my_id>', views.blogPost, name='blogPost'),
    
   
    
]

