from django.urls import path
from tweet import views as v


urlpatterns = [
    path('', v.dashboard, name='dashboard'),
    path('home/', v.homepage, name='homepage'),
    path('create/', v.CreateTweet.as_view(), name='createtweet'),
    path('tweet/<int:tweet_id>/', v.tweet_detail, name='tweetdetail'),
    path('follow/<str:username>/', v.FollowView.as_view(), name='follow'),
    path('unfollow/<str:username>/', v.UnfollowView.as_view(), name='unfollow'),
    path('profile/<str:username>/', v.profile_detail, name='userprofile'),
]
