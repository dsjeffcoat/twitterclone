from django import forms
from .models import Tweet


class TweetForm(forms.ModelForm):
    tweet = forms.CharField(max_length=140)

    class Meta:
        model = Tweet
        fields = ['tweet']
        exclude = ['time', 'user']
