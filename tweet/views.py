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
    all_tweets = Tweet.objects.filter(user=request.user).order_by('-time')
    return render(request, 'dashboard.html', {'feed': all_tweets})


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
    user = TwitterUser.objects.get(username=username)
    tweets = Tweet.objects.filter(user=user)
    return render(request, 'profile.html', {'user': user, 'tweets': tweets})


def follow_view(request, username):
    pass
    # current_user = request.user
    # follow =


def unfollow_view(request, username):
    pass
