from django.urls import path
from tweet import views as v


urlpatterns = [
    path('', v.dashboard, name='dashboard'),
    path('home/', v.homepage, name='homepage'),
    path('create/', v.create_tweet, name='createtweet'),
    path('follow/<str:username>/', v.follow_view, name='follow'),
    path('unfollow/<str:username>/', v.unfollow_view, name='unfollow'),
    path('profile/<str:username>/', v.profile_detail, name='userprofile'),
]
