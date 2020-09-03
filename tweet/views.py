from django.shortcuts import render, HttpResponseRedirect, reverse
from .forms import TweetForm
from .models import Tweet
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def dashboard(request):
    all_tweets = Tweet.objects.all().order_by('-time')
    return render(request, 'twitterfeed.html', {'feed': all_tweets})


@login_required
def create_tweet(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post = Tweet.objects.create(
                tweet=data.get('tweet')
            )
            return render(request, 'create_tweet.html', {'tweet': post})

    form = TweetForm()
    return render(request, 'create_tweet.html', {'form': form})
