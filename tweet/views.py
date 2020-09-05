from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import TweetForm
from .models import Tweet
from twitteruser.models import TwitterUser
from django.contrib.auth.decorators import login_required


# Create your views here.

def homepage(request):
    return render(request, 'index.html')


@login_required
def dashboard(request):
    user = Tweet.objects.filter(user=request.user)
    following = Tweet.objects.filter(user__in=request.user.following.all())
    feed = user | following
    feed = feed.order_by('-time')
    return render(request, 'dashboard.html', {'feed': feed})


@login_required
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post = Tweet.objects.create(
                tweet=data.get('tweet'),
                user=request.user,
            )
            return HttpResponseRedirect(reverse('dashboard'))

    form = TweetForm()
    return render(request, 'create_tweet.html', {'form': form})


def profile_detail(request, username):
    user = TwitterUser.objects.filter(username=username).first()
    tweets = Tweet.objects.filter(user=user).order_by('-time')
    # TODO: Add Notification count here
    if request.user.is_authenticated:
        following = request.user.following.all()
    else:
        following = []
    return render(request, 'profile.html', {'user': user, 'tweets': tweets, 'following': following})


def follow_view(request, username):
    current_user = request.user
    follow_user = TwitterUser.objects.filter(username=username).first()
    current_user.following.add(follow_user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def unfollow_view(request, username):
    current_user = request.user
    follow_user = TwitterUser.objects.filter(username=username).first()
    current_user.following.remove(follow_user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
