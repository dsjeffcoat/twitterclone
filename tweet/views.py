from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import TweetForm
from .models import Tweet
from twitteruser.models import TwitterUser
from notifications.models import Notification
from notifications import views
from django.contrib.auth.decorators import login_required
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
import re

# Create your views here.


def homepage(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    user = Tweet.objects.filter(user=request.user)
    following = Tweet.objects.filter(user__in=request.user.following.all())
    notifications = views.notification_count_view(request)
    feed = user | following
    feed = feed.order_by('-time')
    return render(request, 'dashboard.html', {'feed': feed, 'notifications': notifications})


class CreateTweet(LoginRequiredMixin, TemplateView):

    def get(self, request):
        notifications = views.notification_count_view(request)
        form = TweetForm()
        return render(request, 'create_tweet.html', {'form': form})

    def post(self, request):
        notifications = views.notification_count_view(request)
        form = TweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post = Tweet.objects.create(
                tweet=data.get('tweet'),
                user=request.user,
            )
            mentions = re.findall(r'@(\w+)', data.get('tweet'))
            if mentions:
                for mention in mentions:
                    tagged_user = TwitterUser.objects.get(username=mention)
                    if tagged_user:
                        Notification.objects.create(
                            mentioned=tagged_user,
                            mention_tweet=post
                        )
            return HttpResponseRedirect(reverse('dashboard'), {'notifications': notifications})
        else:
            return render(request, 'create_tweet.html', {'form': form})


# @login_required
# def create_tweet(request):
#     notifications = views.notification_count_view(request)
#     if request.method == 'POST':
#         form = TweetForm(request.POST)
#         if form.is_valid():
#             data = form.cleaned_data
#             post = Tweet.objects.create(
#                 tweet=data.get('tweet'),
#                 user=request.user,
#             )
#             mentions = re.findall(r'@(\w+)', data.get('tweet'))
#             if mentions:
#                 for mention in mentions:
#                     tagged_user = TwitterUser.objects.get(username=mention)
#                     if tagged_user:
#                         Notification.objects.create(
#                             mentioned=tagged_user,
#                             mention_tweet=post
#                         )
#             return HttpResponseRedirect(reverse('dashboard'), {'notifications': notifications})

#     form = TweetForm()
#     return render(request, 'create_tweet.html', {'form': form})


def tweet_detail(request, tweet_id):
    tweet = Tweet.objects.get(id=tweet_id)
    return render(request, 'tweet.html', {'tweet': tweet})


def profile_detail(request, username):
    user = TwitterUser.objects.filter(username=username).first()
    tweets = Tweet.objects.filter(user=user).order_by('-time')
    notifications = views.notification_count_view(request)
    if request.user.is_authenticated:
        following = request.user.following.all()
    else:
        following = []
    return render(request, 'profile.html', {'user': user, 'tweets': tweets, 'following': following, 'notifications': notifications})


# def follow_view(request, username):
#     current_user = request.user
#     follow_user = TwitterUser.objects.filter(username=username).first()
#     current_user.following.add(follow_user)
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

class FollowView(TemplateView):
    def get(self, request, username):
        current_user = request.user
        follow_user = TwitterUser.objects.filter(username=username).first()
        current_user.following.add(follow_user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UnfollowView(TemplateView):
    def get(self, request, username):
        current_user = request.user
        follow_user = TwitterUser.objects.filter(username=username).first()
        current_user.following.remove(follow_user)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

# def unfollow_view(request, username):
#     current_user = request.user
#     follow_user = TwitterUser.objects.filter(username=username).first()
#     current_user.following.remove(follow_user)
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
